from typing import Dict, Optional, Iterable

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.monkeypatch import MonkeyPatch
from flask import Blueprint, Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
# noinspection PyPackageRequirements
from google.auth.exceptions import GoogleAuthError
# noinspection PyPackageRequirements
from google.oauth2 import id_token

from app import app, configure_app
from src.auth.auth_bp import LoginRequest, LoginResponse, auth_role
from src.auth.auth_service import AuthService
from src.config import EnvironmentConstantsKeys
from src.user.user_dto import UserInfoDTO
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest


class TestLogin(DatabaseTest):
    MOCK_GOOGLE_TOKEN = 'testcredential'
    MOCK_GOOGLE_CLIENT_ID = 'google_client_id'
    MOCK_GOOGLE_RESPONSE = dict(email='admin@stc.com', name='Admin', picture='')

    MOCK_ACCESS_TOKEN = 'mockjwtaccesstoken'

    def mock_google_auth_token_verifier(self, monkeypatch: MonkeyPatch, response: Optional[Dict[str, any]] = None,
                                        error: Optional[Exception] = None):
        # noinspection PyUnusedLocal,PyShadowingNames
        def mock_verify_oauth2_token(id_token, request, audience, clock_skew_in_seconds) -> Dict[str, any]:
            if error:
                raise error
            assert id_token == self.MOCK_GOOGLE_TOKEN
            assert audience == self.MOCK_GOOGLE_CLIENT_ID
            return response if response else self.MOCK_GOOGLE_RESPONSE

        monkeypatch.setattr(id_token, 'verify_oauth2_token', mock_verify_oauth2_token)

    @pytest.fixture(autouse=True)
    def setup_mocks(self, monkeypatch: MonkeyPatch) -> None:
        def mock_create_access_token(identity) -> str:
            return self.MOCK_ACCESS_TOKEN

        with app.app_context():
            UserService.add_user(self.MOCK_GOOGLE_RESPONSE['email'], [UserRole.ADMIN])
        monkeypatch.setenv(EnvironmentConstantsKeys.GOOGLE_LOGIN_CLIENT_ID, self.MOCK_GOOGLE_CLIENT_ID)
        self.mock_google_auth_token_verifier(monkeypatch)
        monkeypatch.setattr(AuthService, 'create_access_token', mock_create_access_token)

    def test_successful_login(self, monkeypatch: MonkeyPatch, client: FlaskClient):
        response = client.post('/auth/login', json=LoginRequest(credential=self.MOCK_GOOGLE_TOKEN))

        assert response.status_code == 200
        actual_response = LoginResponse.model_validate(response.json)
        expected_response = LoginResponse(
            user=UserInfoDTO(
                email=self.MOCK_GOOGLE_RESPONSE['email'],
                name=self.MOCK_GOOGLE_RESPONSE['name'],
                picture_url=self.MOCK_GOOGLE_RESPONSE['picture'],
                roles=[UserRole.ADMIN.value],
            ),
            access_token=self.MOCK_ACCESS_TOKEN,
        )
        assert actual_response.user == expected_response.user

    def test_invalid_user(self, monkeypatch: MonkeyPatch, client: FlaskClient):
        self.mock_google_auth_token_verifier(
            monkeypatch,
            {**self.MOCK_GOOGLE_RESPONSE, **dict(email='unknown-user@gmail.com')})

        response = client.post('/auth/login', json=LoginRequest(credential=self.MOCK_GOOGLE_TOKEN))

        assert response.status_code == 403
        assert response.json == dict(message='Not a known user: unknown-user@gmail.com')

    def test_invalid_request(self, monkeypatch: MonkeyPatch, client: FlaskClient):
        response = client.post('/auth/login', json={"junk_data": "nothing meaningful"})

        assert response.status_code == 400
        assert 'message' in response.json
        assert 'Invalid request' in response.json['message']

    @pytest.mark.parametrize('error', [GoogleAuthError(), ValueError()])
    def test_google_auth_failed(self, monkeypatch: MonkeyPatch, client: FlaskClient, error: Exception):
        self.mock_google_auth_token_verifier(monkeypatch, error=error)

        response = client.post('/auth/login', json=LoginRequest(credential=self.MOCK_GOOGLE_TOKEN))

        assert response.status_code == 400
        assert 'message' in response.json
        assert 'Token verification failed' in response.json['message']

    @pytest.mark.parametrize('absent_field', ['name', 'picture'])
    def test_inaccessible_google_profile(self, monkeypatch: MonkeyPatch, client: FlaskClient,
                                         absent_field: str):
        self.mock_google_auth_token_verifier(
            monkeypatch,
            response={k: v for k, v in self.MOCK_GOOGLE_RESPONSE.items() if k != absent_field})

        response = client.post('/auth/login', json=LoginRequest(credential=self.MOCK_GOOGLE_TOKEN))

        assert response.status_code == 400
        assert 'message' in response.json
        assert 'User profile not accessible, field not found' in response.json['message']
        assert absent_field in response.json['message']


class TestAuthorization(DatabaseTest):
    ADMIN_EMAIL = 'admin@stc.com'
    CARBON_AUDITOR_EMAIL = 'ca@stc.com'

    @pytest.fixture(scope="class")
    def auth_app(self):
        auth_test_bp = Blueprint('test-authorization', __name__, url_prefix='/test-authorization/')

        @auth_test_bp.route('/admin', methods=['GET'])
        @auth_role(UserRole.ADMIN)
        def get_admin():
            return 'Success'

        @auth_test_bp.route('/admin-async', methods=['GET'])
        @auth_role(UserRole.ADMIN)
        async def get_admin_async():
            return 'Success'

        @auth_test_bp.route('/carbon-auditor', methods=['GET'])
        @auth_role(UserRole.CARBON_AUDITOR)
        def get_carbon_auditor():
            return 'Success'

        @auth_test_bp.route('/admin-or-ca', methods=['GET'])
        @auth_role(UserRole.CARBON_AUDITOR, UserRole.ADMIN)
        def get_carbon_auditor_and_admin():
            return 'Success'

        auth_app = Flask('authorization-app')
        configure_app(auth_app)
        auth_app.register_blueprint(auth_test_bp)
        return auth_app

    @pytest.fixture(scope="class")
    def auth_client(self, auth_app) -> FlaskClient:
        return auth_app.test_client()

    @staticmethod
    def create_access_token(auth_app: Flask, email: str, roles: Iterable[UserRole]):
        with auth_app.app_context():
            access_token = create_access_token(email, additional_claims=AuthService.build_claims_for_roles(roles))
        return access_token

    @pytest.fixture
    def access_headers_admin(self, auth_app) -> Dict[str, str]:
        access_token = TestAuthorization.create_access_token(auth_app, TestAuthorization.ADMIN_EMAIL, [UserRole.ADMIN])
        return {'Authorization': f'Bearer {access_token}'}

    @pytest.fixture
    def access_headers_carbon_auditor(self, auth_app) -> Dict[str, str]:
        access_token = TestAuthorization.create_access_token(
            auth_app,
            TestAuthorization.CARBON_AUDITOR_EMAIL,
            [UserRole.CARBON_AUDITOR]
        )
        return {'Authorization': f'Bearer {access_token}'}

    @pytest.fixture
    def access_headers_nobody(self, auth_app) -> Dict[str, str]:
        return {}

    @pytest.mark.parametrize('target', ['admin', 'admin-async'])
    @pytest.mark.parametrize('code, headers', [
        (200, 'access_headers_admin'),
        (403, 'access_headers_carbon_auditor'),
        (401, 'access_headers_nobody'),
    ])
    def test_admin(self, auth_client: FlaskClient, request: FixtureRequest, target: str, code: int, headers: str):
        response = auth_client.get(f'/test-authorization/{target}', headers=request.getfixturevalue(headers))
        assert response.status_code == code

    @pytest.mark.parametrize('code, headers', [
        (403, 'access_headers_admin'),
        (200, 'access_headers_carbon_auditor'),
        (401, 'access_headers_nobody'),
    ])
    def test_carbon_auditor(self, auth_client: FlaskClient, request: FixtureRequest, code: int, headers: str):
        response = auth_client.get('/test-authorization/carbon-auditor', headers=request.getfixturevalue(headers))
        assert response.status_code == code

    @pytest.mark.parametrize('code, headers', [
        (200, 'access_headers_admin'),
        (200, 'access_headers_carbon_auditor'),
        (401, 'access_headers_nobody'),
    ])
    def test_admin_or_carbon_auditor(self, auth_client: FlaskClient, request: FixtureRequest, code: int, headers: str):
        response = auth_client.get('/test-authorization/admin-or-ca', headers=request.getfixturevalue(headers))
        assert response.status_code == code

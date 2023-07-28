from typing import Dict, Optional

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask.testing import FlaskClient
# noinspection PyPackageRequirements
from google.auth.exceptions import GoogleAuthError
# noinspection PyPackageRequirements
from google.oauth2 import id_token

from app import app
from src.auth import auth_bp
from src.auth.auth_bp import LoginRequest
from src.auth.auth_role import AuthRole
from src.auth.auth_service import AuthService
from src.config import EnvironmentConstantsKeys
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
            AuthService.add_user(self.MOCK_GOOGLE_RESPONSE['email'], [AuthRole.ADMIN])
        monkeypatch.setenv(EnvironmentConstantsKeys.GOOGLE_LOGIN_CLIENT_ID, self.MOCK_GOOGLE_CLIENT_ID)
        self.mock_google_auth_token_verifier(monkeypatch)
        monkeypatch.setattr(auth_bp, 'create_access_token', mock_create_access_token)

    def test_successful_login(self, monkeypatch: MonkeyPatch, client: FlaskClient):
        response = client.post('/auth/login', json=LoginRequest(credential=self.MOCK_GOOGLE_TOKEN))

        assert response.status_code == 200
        assert response.json == dict(
            email=self.MOCK_GOOGLE_RESPONSE['email'],
            name=self.MOCK_GOOGLE_RESPONSE['name'],
            picture_url=self.MOCK_GOOGLE_RESPONSE['picture'],
            access_token=self.MOCK_ACCESS_TOKEN,
            roles=[AuthRole.ADMIN.value],
        )

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

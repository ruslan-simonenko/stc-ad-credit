from typing import Dict, Callable

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask.testing import FlaskClient

from app import app
from src.auth.auth_service import AuthService
from src.user import user_bp
from src.user.user_dto import UserInfoDTO, UsersGetManageableResponse, UserAddForm, UserAddSuccessfulResponse
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest

CURRENT_ADMIN_EMAIL = 'admin@stc.com'
USER_A_EMAIL = 'carbon-auditorA@stc.com'
USER_B_EMAIL = 'carbon-auditorB@stc.com'
ANOTHER_ADMIN_EMAIL = 'another-admin@stc.com'


class TestUserEndpoint:

    @staticmethod
    def mock_normalize_email(monkeypatch: MonkeyPatch, normalizer: Callable[[str], str]):
        async def normalize_email_mock(email: str) -> str:
            return normalizer(email)

        monkeypatch.setattr(user_bp, 'normalize_email', normalize_email_mock)

    @pytest.fixture(autouse=True)
    def setup_normalize_email_mock(self, monkeypatch: MonkeyPatch):
        TestUserEndpoint.mock_normalize_email(monkeypatch, lambda x: x)

    @pytest.fixture
    def access_headers(self) -> Dict[str, str]:
        with app.app_context():
            UserService.add_user(CURRENT_ADMIN_EMAIL, [UserRole.ADMIN])
            access_token = AuthService.create_access_token(CURRENT_ADMIN_EMAIL)
        return {'Authorization': f'Bearer {access_token}'}

    class TestGetManageableUsers(DatabaseTest):

        def test_no_users(self, client: FlaskClient, access_headers: Dict[str, str]):
            response = client.get('/users/manageable', headers=access_headers)

            assert response.status_code == 200
            assert response.json == dict(
                users=list()
            )

        def test_returns_only_carbon_auditors(self, client: FlaskClient, access_headers: Dict[str, str]):
            with app.app_context():
                UserService.add_user(USER_A_EMAIL, [UserRole.CARBON_AUDITOR])
                UserService.add_user(USER_B_EMAIL, [UserRole.CARBON_AUDITOR])
                UserService.add_user(ANOTHER_ADMIN_EMAIL, [UserRole.ADMIN])

            response = client.get('/users/manageable', headers=access_headers)

            assert response.status_code == 200
            actual_response = UsersGetManageableResponse.model_validate(response.json)
            expected_response = UsersGetManageableResponse(
                users=[UserInfoDTO(email=USER_A_EMAIL, roles=[UserRole.CARBON_AUDITOR]),
                       UserInfoDTO(email=USER_B_EMAIL, roles=[UserRole.CARBON_AUDITOR])])
            assert actual_response == expected_response

    class TestAddUser(DatabaseTest):

        def test_simple_add(self, client: FlaskClient, access_headers: Dict[str, str]):
            response = client.post('/users/',
                                   json=UserAddForm(email=USER_A_EMAIL, roles=[UserRole.CARBON_AUDITOR]),
                                   headers=access_headers)

            assert response.status_code == 200
            actual_response = UserAddSuccessfulResponse.model_validate(response.json)
            expected_response = UserAddSuccessfulResponse(
                user=UserInfoDTO(email=USER_A_EMAIL, roles=[UserRole.CARBON_AUDITOR]))
            assert actual_response == expected_response

        def test_email_normalization(self, client: FlaskClient, access_headers: Dict[str, str],
                                     monkeypatch: MonkeyPatch):
            def normalize_email(email):
                return f'normalized-{email}'

            TestUserEndpoint.mock_normalize_email(monkeypatch, normalize_email)

            response = client.post('/users/',
                                   json=UserAddForm(email=USER_A_EMAIL, roles=[UserRole.CARBON_AUDITOR]),
                                   headers=access_headers)

            assert response.status_code == 200
            actual_response = UserAddSuccessfulResponse.model_validate(response.json)
            expected_response = UserAddSuccessfulResponse(
                user=UserInfoDTO(email=normalize_email(USER_A_EMAIL), roles=[UserRole.CARBON_AUDITOR]))
            assert actual_response == expected_response

    class TestAddAndGetUsers(DatabaseTest):
        def test_add_and_get_users(self, client: FlaskClient, access_headers: Dict[str, str]):
            for user_email in [USER_A_EMAIL, USER_B_EMAIL]:
                client.post('/users/',
                            json=UserAddForm(email=user_email, roles=[UserRole.CARBON_AUDITOR]),
                            headers=access_headers)

            response = client.get('/users/manageable', headers=access_headers)

            assert response.status_code == 200
            actual_response = UsersGetManageableResponse.model_validate(response.json)
            expected_response = UsersGetManageableResponse(
                users=[UserInfoDTO(email=USER_A_EMAIL, roles=[UserRole.CARBON_AUDITOR]),
                       UserInfoDTO(email=USER_B_EMAIL, roles=[UserRole.CARBON_AUDITOR])])
            assert actual_response == expected_response

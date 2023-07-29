from typing import Dict

import pytest
from flask.testing import FlaskClient

from app import app
from src.auth.auth_service import AuthService
from src.user.user_dto import UserInfoDTO, UsersGetManageableResponse
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest


class TestUserEndpoint:

    @pytest.fixture(scope="class")
    def access_headers(self) -> Dict[str, str]:
        with app.app_context():
            access_token = AuthService.create_access_token('admin@stc.com')
        return {'Authorization': f'Bearer {access_token}'}

    class TestGetManageableUsers(DatabaseTest):

        def test_no_users(self, client: FlaskClient, access_headers: Dict[str, str]):
            response = client.get('/users/manageable', headers=access_headers)

            assert response.status_code == 200
            assert response.json == dict(
                users=list()
            )

        def test_returns_only_carbon_auditors(self, client: FlaskClient, access_headers: Dict[str, str]):
            user_a_email = 'carbon-auditorA@stc.com'
            user_b_email = 'carbon-auditorB@stc.com'
            another_admin_email = 'another-admin@stc.com'
            with app.app_context():
                UserService.add_user(user_a_email, [UserRole.CARBON_AUDITOR])
                UserService.add_user(user_b_email, [UserRole.CARBON_AUDITOR])
                UserService.add_user(another_admin_email, [UserRole.ADMIN])

            response = client.get('/users/manageable', headers=access_headers)

            assert response.status_code == 200
            actual_response = UsersGetManageableResponse.model_validate(response.json)
            expected_response = UsersGetManageableResponse(
                users=[UserInfoDTO(email=user_a_email, roles=[UserRole.CARBON_AUDITOR]),
                       UserInfoDTO(email=user_b_email, roles=[UserRole.CARBON_AUDITOR])])
            assert actual_response == expected_response

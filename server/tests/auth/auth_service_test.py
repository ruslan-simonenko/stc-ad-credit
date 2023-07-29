import pytest
from src.user.user_types import UserRole, UserInfo
from src.auth.auth_service import AuthService

from app import app
from tests.persistence.db_test import DatabaseTest


class TestAuthRoleService(DatabaseTest):
    TEST_USER_EMAIL = 'test-user@gmail.com'

    def test_add_admin(self):
        with app.app_context():
            AuthService.add_user(self.TEST_USER_EMAIL, [UserRole.ADMIN])
            actual_roles = AuthService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == [UserRole.ADMIN]

    def test_add_without_roles_fails(self):
        with app.app_context():
            with pytest.raises(ValueError, match='At least one role is required'):
                AuthService.add_user(self.TEST_USER_EMAIL, [])

    def test_get_unknown_user(self):
        with app.app_context():
            actual_roles = AuthService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == []

    def test_setup_admin(self):
        with app.app_context():
            AuthService.setup_admin(self.TEST_USER_EMAIL)
            assert AuthService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]

    def test_setup_admin_is_idempotent(self):
        with app.app_context():
            AuthService.setup_admin(self.TEST_USER_EMAIL)
            assert AuthService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]
            AuthService.setup_admin(self.TEST_USER_EMAIL)
            AuthService.setup_admin(self.TEST_USER_EMAIL)
            assert AuthService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]

    def test_get_users(self):
        with app.app_context():
            AuthService.add_user('userA@gmail.com', [UserRole.ADMIN, UserRole.CARBON_AUDITOR])
            AuthService.add_user('userB@gmail.com', [UserRole.CARBON_AUDITOR])
            users = AuthService.get_users()
            assert set(users) == {
                UserInfo(email='userA@gmail.com', roles=tuple([UserRole.ADMIN, UserRole.CARBON_AUDITOR])),
                UserInfo(email='userB@gmail.com', roles=tuple([UserRole.CARBON_AUDITOR]))
            }

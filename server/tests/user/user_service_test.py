import pytest

from app import app
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest


class TestUserService(DatabaseTest):
    TEST_USER_EMAIL = 'test-user@gmail.com'

    def test_add_admin(self):
        with app.app_context():
            UserService.add_user(self.TEST_USER_EMAIL, [UserRole.ADMIN])
            actual_roles = UserService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == [UserRole.ADMIN]

    def test_add_without_roles_fails(self):
        with app.app_context():
            with pytest.raises(ValueError, match='At least one role is required'):
                UserService.add_user(self.TEST_USER_EMAIL, [])

    def test_get_unknown_user(self):
        with app.app_context():
            actual_roles = UserService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == []

    def test_setup_admin(self):
        with app.app_context():
            UserService.setup_admin(self.TEST_USER_EMAIL)
            assert UserService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]

    def test_setup_admin_is_idempotent(self):
        with app.app_context():
            UserService.setup_admin(self.TEST_USER_EMAIL)
            assert UserService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]
            UserService.setup_admin(self.TEST_USER_EMAIL)
            UserService.setup_admin(self.TEST_USER_EMAIL)
            assert UserService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]

    def test_get_users(self):
        with app.app_context():
            user_a = UserService.add_user('userA@gmail.com', [UserRole.ADMIN, UserRole.CARBON_AUDITOR])
            user_b = UserService.add_user('userB@gmail.com', [UserRole.CARBON_AUDITOR])
            users = UserService.get_users()
            assert user_a in users
            assert user_b in users

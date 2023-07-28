import pytest
from src.auth.auth_role import AuthRole
from src.auth.auth_service import AuthService

from app import app
from tests.persistence.db_test import DatabaseTest


class TestAuthRoleService(DatabaseTest):
    TEST_USER_EMAIL = 'test-user@gmail.com'

    def test_add_admin(self):
        with app.app_context():
            AuthService.add_user(self.TEST_USER_EMAIL, [AuthRole.ADMIN])
            actual_roles = AuthService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == [AuthRole.ADMIN]

    def test_add_without_roles_fails(self):
        with app.app_context():
            with pytest.raises(ValueError, match='At least one role is required'):
                AuthService.add_user(self.TEST_USER_EMAIL, [])

    def test_get_unknown_user(self):
        with app.app_context():
            actual_roles = AuthService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == []

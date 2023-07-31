from typing import Iterable

import pytest

from app import app
from src.persistence.schema.role import Role
from src.persistence.schema.user import User
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest


class TestUserService(DatabaseTest):
    TEST_USER_EMAIL = 'test-user@gmail.com'

    @pytest.fixture(autouse=True)
    def setup_app_context(self):
        with app.app_context():
            yield

    def test_add_admin(self):
        UserService.add_user(self.TEST_USER_EMAIL, [UserRole.ADMIN])
        actual_roles = UserService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == [UserRole.ADMIN]

    def test_get_unknown_user(self):
        actual_roles = UserService.get_user_roles(self.TEST_USER_EMAIL)
        assert actual_roles == []

    def test_setup_admin(self):
        UserService.setup_admin(self.TEST_USER_EMAIL)
        assert UserService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]

    def test_setup_admin_is_idempotent(self):
        UserService.setup_admin(self.TEST_USER_EMAIL)
        assert UserService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]
        UserService.setup_admin(self.TEST_USER_EMAIL)
        UserService.setup_admin(self.TEST_USER_EMAIL)
        assert UserService.get_user_roles(self.TEST_USER_EMAIL) == [UserRole.ADMIN]

    def test_get_users(self):
        user_a = UserService.add_user('userA@gmail.com', [UserRole.ADMIN, UserRole.CARBON_AUDITOR])
        user_b = UserService.add_user('userB@gmail.com', [UserRole.CARBON_AUDITOR])
        users = UserService.get_users()
        assert user_a in users
        assert user_b in users

    class TestRoles:

        @pytest.mark.parametrize('roles, new_roles', [
            ([], [UserRole.ADMIN, UserRole.CARBON_AUDITOR]),
            ([UserRole.ADMIN, UserRole.CARBON_AUDITOR], []),
            ([UserRole.ADMIN], [UserRole.CARBON_AUDITOR]),
        ])
        def test_set_roles(self, roles: Iterable[UserRole], new_roles: Iterable[UserRole]):
            user = UserService.add_user('user@gmail.com', roles)

            updated_user = UserService.set_user_roles(user.id, new_roles)
            assert _get_user_roles(updated_user) == new_roles

            user = UserService.get_user_by_id(user.id)
            assert _get_user_roles(user) == new_roles

        def test_role_change_has_no_effect_on_other_users(self):
            user_a = UserService.add_user('userA@gmail.com', [UserRole.ADMIN, UserRole.CARBON_AUDITOR])
            user_b = UserService.add_user('userB@gmail.com', [UserRole.CARBON_AUDITOR])

            updated_user_a = UserService.set_user_roles(user_a.id, [])
            assert updated_user_a.roles == []

            user_a = UserService.get_user_by_id(user_a.id)
            user_b = UserService.get_user_by_id(user_b.id)
            assert user_a.roles == []
            assert len(user_b.roles) == 1
            assert user_b.roles[0].name == UserRole.CARBON_AUDITOR.value

        def test_set_non_existing_user_roles(self):
            user_a = UserService.add_user('userA@gmail.com', [UserRole.ADMIN, UserRole.CARBON_AUDITOR])
            user_b = UserService.add_user('userB@gmail.com', [UserRole.CARBON_AUDITOR])
            with pytest.raises(ValueError, match='User does not exist'):
                UserService.set_user_roles(-1, [UserRole.ADMIN])

            assert UserService.get_user_roles(user_a.email) == [UserRole.ADMIN, UserRole.CARBON_AUDITOR]
            assert UserService.get_user_roles(user_b.email) == [UserRole.CARBON_AUDITOR]


def _get_user_roles(user: User) -> Iterable[UserRole]:
    return [UserRole(role.name) for role in user.roles]

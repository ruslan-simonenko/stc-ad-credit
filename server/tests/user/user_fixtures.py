from typing import NamedTuple

import pytest

from src.persistence.schema.user import User
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.app_fixtures import AppContextFixture


class UserFixtures(AppContextFixture):
    USER_ADMIN_EMAIL = 'admin@stc.org'
    USER_AD_MANAGER_EMAIL = 'ad-manager@stc.org'
    USER_BUSINESS_MANAGER_EMAIL = 'business-manager@stc.org'
    USER_CARBON_AUDITOR_EMAIL = 'carbon-auditor@stc.org'
    USER_ALL_ROLES_EMAIL = 'jack-of-all-trades@stc.org'

    class Users(NamedTuple):
        admin: User
        ad_manager: User
        business_manager: User
        carbon_auditor: User
        all_roles: User

    @pytest.fixture
    def users(self, app_context) -> Users:
        admin = UserService.add_user(self.USER_ADMIN_EMAIL, [UserRole.ADMIN])
        ad_manager = UserService.add_user(self.USER_AD_MANAGER_EMAIL, [UserRole.AD_MANAGER])
        business_manager = UserService.add_user(self.USER_BUSINESS_MANAGER_EMAIL, [UserRole.BUSINESS_MANAGER])
        carbon_auditor = UserService.add_user(self.USER_CARBON_AUDITOR_EMAIL, [UserRole.CARBON_AUDITOR])
        all_roles = UserService.add_user(self.USER_ALL_ROLES_EMAIL,
                                         [UserRole.ADMIN, UserRole.AD_MANAGER, UserRole.BUSINESS_MANAGER,
                                          UserRole.CARBON_AUDITOR])
        return self.Users(admin=admin, ad_manager=ad_manager, business_manager=business_manager,
                          carbon_auditor=carbon_auditor, all_roles=all_roles)

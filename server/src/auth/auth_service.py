import os
from typing import List

from src.auth.auth_role import AuthRole
from src.config import EnvironmentConstantsKeys


class AuthService:

    @staticmethod
    def get_user_roles(email: str) -> List[AuthRole]:
        try:
            project_manager_email = os.environ[EnvironmentConstantsKeys.PROJECT_MANAGER_EMAIL]
        except KeyError as e:
            raise RuntimeError(f'Invalid configuration: environment variable {e.args[0]} is not set')
        if email == project_manager_email:
            return [AuthRole.ADMIN]
        return []

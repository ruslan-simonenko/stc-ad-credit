from typing import Dict, Iterable, Set, List, Optional

from flask_jwt_extended import create_access_token, get_jwt

from src.user.user_service import UserService
from src.user.user_types import UserRole

CLAIM_KEY_ROLES = "stc-roles"


class AuthService:
    @staticmethod
    def create_access_token(email: str):
        user_roles = UserService.get_user_roles(email)
        return create_access_token(email, additional_claims=AuthService.build_claims_for_roles(user_roles))

    @staticmethod
    def get_roles_from_claims() -> Set[UserRole]:
        claims = get_jwt()
        return {UserRole(role) for role in claims[CLAIM_KEY_ROLES].split(':')}

    @staticmethod
    def build_claims_for_roles(roles: Iterable[UserRole]) -> Dict[str, str]:
        return {CLAIM_KEY_ROLES: ':'.join(roles)}

from typing import Dict, Iterable, Set, List, Optional

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity

from src.persistence.schema.user import User
from src.user.user_service import UserService
from src.user.user_types import UserRole

CLAIM_KEY_ROLES = "stc-roles"


class AuthService:
    @staticmethod
    def create_access_token(user_id: int):
        user = UserService.get_user_by_id(user_id)
        return create_access_token(user_id, additional_claims=AuthService.build_roles_claim(user))

    @staticmethod
    def get_current_user_id_or_throw() -> User:
        user_id = get_jwt_identity()
        if not user_id:
            raise RuntimeError('Not in the context of request, or the endpoint does not require authentication.')
        return user_id

    @staticmethod
    def get_roles_from_claims() -> Set[UserRole]:
        claims = get_jwt()
        return {UserRole(role) for role in claims[CLAIM_KEY_ROLES].split(':')}

    @staticmethod
    def build_roles_claim(user: User) -> Dict[str, str]:
        return {CLAIM_KEY_ROLES: ':'.join([role.name for role in user.roles])}

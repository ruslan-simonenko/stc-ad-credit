import os
from typing import List, Iterable

from src.auth.auth_role import AuthRole
from src.config import EnvironmentConstantsKeys
from src.persistence.schema import User, UserRole, db, Role


class AuthService:

    @staticmethod
    def add_user(email: str, roles: Iterable[AuthRole]) -> User:
        if not roles:
            raise ValueError('At least one role is required')
        with db.session.begin_nested():
            user = User(email=email)
            db.session.add(user)

            roles = Role.query.filter(Role.name.in_([role.value for role in roles]))
            for role in roles:
                user_role = UserRole(user=user, role=role)
                db.session.add(user_role)

            db.session.commit()
        return user

    @staticmethod
    def get_user_roles(email: str) -> List[AuthRole]:
        try:
            project_manager_email = os.environ[EnvironmentConstantsKeys.PROJECT_MANAGER_EMAIL]
        except KeyError as e:
            raise RuntimeError(f'Invalid configuration: environment variable {e.args[0]} is not set')
        if email == project_manager_email:
            return [AuthRole.ADMIN]

        user = User.query.filter_by(email=email).first()
        if not user:
            return []
        user_roles = UserRole.query.filter_by(user_id=user.id).all()
        role_names = [user_role.role.name for user_role in user_roles]
        return [AuthRole(role_name) for role_name in role_names]


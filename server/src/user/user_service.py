from typing import Iterable, List, Optional

from sqlalchemy import select

from src.persistence.schema import db
from src.persistence.schema.role import Role
from src.persistence.schema.user import User
from src.persistence.schema.user_role import UserRole as UserRoleEntity
from src.user.user_types import UserRole


class UserService:

    @staticmethod
    def add_user(email: str, roles: Iterable[UserRole]) -> User:
        with db.session.begin_nested():
            user = User(email=email)
            db.session.add(user)
            UserService._add_user_roles(user, roles)
            db.session.commit()
        return user

    @staticmethod
    def set_user_roles(user_id: int, roles: Iterable[UserRole]) -> User:
        with db.session.begin_nested():
            user = UserService.get_user_by_id(user_id)
            if not user:
                raise ValueError(f'User does not exist: {user_id}')
            for user_role in user.user_roles:
                db.session.delete(user_role)
            UserService._add_user_roles(user, roles)
        db.session.refresh(user)
        return UserService.get_user_by_id(user_id)

    @staticmethod
    def _add_user_roles(user: User, roles: Iterable[UserRole]):
        role_entities = Role.query.filter(Role.name.in_([role.value for role in roles]))
        for role in role_entities:
            user_role = UserRoleEntity(user=user, role=role)
            db.session.add(user_role)

    @staticmethod
    def get_users(filter_email: Optional[str] = None,
                  filter_id: Optional[int] = None) -> List[User]:
        statement = select(User).outerjoin_from(User, UserRoleEntity).outerjoin(Role)
        if filter_email:
            statement = statement.where(User.email == filter_email)
        if filter_id:
            statement = statement.where(User.id == filter_id)
        return db.session.execute(statement).scalars().all()

    @staticmethod
    def get_user_by_id(id_: int) -> Optional[User]:
        users = UserService.get_users(filter_id=id_)
        return None if not users else users[0]

    @staticmethod
    def get_user(email: str) -> Optional[User]:
        users = UserService.get_users(filter_email=email)
        return None if not users else users[0]

    @staticmethod
    def get_user_roles(email: str) -> List[UserRole]:
        user = User.query.filter_by(email=email).first()
        if not user:
            return []
        return [UserRole(role.name) for role in user.roles]

    @staticmethod
    def update_user(user_id: int, email: Optional[str] = None, roles: Optional[List[UserRole]] = None,
                    avatar_url: Optional[str] = None, name: Optional[str] = None) -> User:
        with db.session.begin_nested():
            user = UserService.get_user_by_id(user_id)
            if email is not None:
                user.email = email
            if roles is not None:
                UserService.set_user_roles(user.id, roles)
            if avatar_url is not None:
                user.avatar_url = avatar_url
            if name is not None:
                user.name = name
        return UserService.get_user_by_id(user_id)

    @staticmethod
    def setup_admin(email: str) -> None:
        current_roles = UserService.get_user_roles(email)
        if UserRole.ADMIN not in current_roles:
            UserService.add_user(email, [UserRole.ADMIN])

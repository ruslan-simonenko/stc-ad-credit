from typing import Iterable, List, Optional

from sqlalchemy import select, update

from src.persistence.schema import db
from src.persistence.schema.role import Role
from src.persistence.schema.user import User
from src.persistence.schema.user_role import UserRole as UserRoleEntity
from src.user.user_types import UserRole


class UserService:

    @staticmethod
    def add_user(email: str, roles: Iterable[UserRole]) -> User:
        if not roles:
            raise ValueError('At least one role is required')
        with db.session.begin_nested():
            user = User(email=email)
            db.session.add(user)

            roles = Role.query.filter(Role.name.in_([role.value for role in roles]))
            for role in roles:
                user_role = UserRoleEntity(user=user, role=role)
                db.session.add(user_role)

            db.session.commit()
        return user

    @staticmethod
    def disable_user(user_id: int) -> User:
        with db.session.begin_nested():
            user = UserService.get_user_by_id(user_id)
            if not user:
                raise ValueError(f'User does not exist: {user_id}')
            for user_role in user.user_roles:
                db.session.delete(user_role)
            db.session.commit()
        return UserService.get_user_by_id(user_id)

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
    def update_user(user: User, avatar_url: str, name: str) -> User:
        db.session.execute(
            update(User).where(User.email == user.email).values({
                User.name: name,
                User.avatar_url: avatar_url
            })
        )
        db.session.commit()
        return UserService.get_user(user.email)

    @staticmethod
    def setup_admin(email: str) -> None:
        current_roles = UserService.get_user_roles(email)
        if UserRole.ADMIN not in current_roles:
            UserService.add_user(email, [UserRole.ADMIN])

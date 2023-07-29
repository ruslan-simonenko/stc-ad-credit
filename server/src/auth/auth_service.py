from dataclasses import dataclass, field
from itertools import groupby
from typing import List, Iterable, Optional, Tuple

from sqlalchemy import select

from src.user.user_types import UserRole
from src.persistence.schema import User, UserRole as UserRoleEntity, db, Role


@dataclass(eq=True, frozen=True)
class UserInfo:
    email: str
    roles: Tuple[UserRole, ...]
    name: Optional[str] = field(default=None)
    picture_url: Optional[str] = field(default=None)


class AuthService:

    @staticmethod
    def add_user(email: str, roles: Iterable[UserRole]) -> UserInfo:
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
        return UserInfo(email=email, roles=tuple(roles))

    @staticmethod
    def get_users() -> List[UserInfo]:
        rows = db.session.execute(
            select(User, Role.name).outerjoin_from(User, UserRoleEntity).outerjoin(Role)
        ).all()
        return [UserInfo(
            email=user.email,
            roles=tuple(sorted(UserRole(row[1]) for row in user_rows)),
            name=user.name,
            picture_url=user.avatar_url,
        ) for user, user_rows in groupby(rows, lambda row: row[0])]

    @staticmethod
    def get_user_roles(email: str) -> List[UserRole]:
        user = User.query.filter_by(email=email).first()
        if not user:
            return []
        user_roles = UserRoleEntity.query.filter_by(user_id=user.id).all()
        role_names = [user_role.role.name for user_role in user_roles]
        return [UserRole(role_name) for role_name in role_names]

    @staticmethod
    def setup_admin(email: str) -> None:
        current_roles = AuthService.get_user_roles(email)
        if UserRole.ADMIN not in current_roles:
            AuthService.add_user(email, [UserRole.ADMIN])

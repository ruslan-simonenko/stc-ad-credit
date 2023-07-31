from typing import Optional, FrozenSet, Any

from pydantic import BaseModel

from src.persistence.schema.user import User
from src.user.user_types import UserRole
from src.utils.dto_data_comparable import DTODataComparable


class UserInfoDTO(BaseModel, DTODataComparable):
    id: int
    email: str
    roles: FrozenSet[UserRole]
    name: Optional[str] = None
    picture_url: Optional[str] = None

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __eq__(self, other: Any) -> bool:
        return self._data_eq(other) and self.id == other.id

    def _data_hash(self) -> int:
        return self.email.__hash__()

    def _data_eq(self, other: Any) -> bool:
        if not isinstance(other, UserInfoDTO):
            return False
        return (self.email == other.email and
                self.roles == other.roles and
                self.name == other.name and
                self.picture_url == other.picture_url)

    @classmethod
    def from_entity(cls, entity: User) -> "UserInfoDTO":
        return cls(id=entity.id,
                   email=entity.email,
                   name=entity.name,
                   picture_url=entity.avatar_url,
                   roles=[UserRole(role.name) for role in entity.roles])


class UsersGetManageableResponse(BaseModel):
    users: FrozenSet[UserInfoDTO]

    def __hash__(self) -> int:
        return self.users.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UsersGetManageableResponse):
            return False
        return self.users == other.users


class UserAddForm(BaseModel):
    email: str
    roles: FrozenSet[UserRole]

    def __hash__(self) -> int:
        return self.email.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UserAddForm):
            return False
        return (self.email == other.email and
                self.roles == other.roles)


class UserAddFailedResponse(BaseModel):
    message: str

    def __hash__(self) -> int:
        return self.message.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UserAddFailedResponse):
            return False
        return self.message == other.message


class UserAddSuccessfulResponse(BaseModel):
    user: UserInfoDTO

    def __hash__(self) -> int:
        return self.user.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UserAddSuccessfulResponse):
            return False
        return self.user == other.user

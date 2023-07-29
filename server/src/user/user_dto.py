from typing import Optional, FrozenSet, Any

from pydantic import BaseModel

from src.user.user_types import UserRole


class UserInfoDTO(BaseModel):
    email: str
    roles: FrozenSet[UserRole]
    name: Optional[str] = None
    picture_url: Optional[str] = None

    def __hash__(self) -> int:
        return self.email.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UserInfoDTO):
            return False
        return (self.email == other.email and
                self.roles == other.roles and
                self.name == other.name and
                self.picture_url == other.picture_url)


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

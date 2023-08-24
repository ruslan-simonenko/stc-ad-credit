from typing import Any

from pydantic import BaseModel

from src.user.user_dto import UserInfoDTO


class LoginRequest(BaseModel):
    credential: str


class LoginResponse(BaseModel):
    user: UserInfoDTO
    access_token: str

    def __hash__(self) -> int:
        return self.user.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LoginResponse):
            return False
        return (self.user == other.user and
                self.access_token == other.access_token)


class LoginAsRequest(BaseModel):
    user_id: int

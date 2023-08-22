from typing import TypeVar, Generic, Any, FrozenSet

from pydantic import BaseModel

T = TypeVar('T')


class ErrorResponse(BaseModel):
    message: str

    def __hash__(self) -> int:
        return self.message.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ErrorResponse):
            return False
        return self.message == other.message


class ResponseWithObject(BaseModel, Generic[T]):
    object: T

    def __hash__(self) -> int:
        return self.object.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ResponseWithObject):
            return False
        return self.object == other.object


class ResponseWithObjects(BaseModel, Generic[T]):
    objects: FrozenSet[T]

    def __hash__(self) -> int:
        return self.object.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ResponseWithObjects):
            return False
        return self.objects == other.objects

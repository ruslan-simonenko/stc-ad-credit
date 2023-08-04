from typing import FrozenSet, Any, Optional

from pydantic import BaseModel

from src.persistence.schema.business import Business
from src.utils.dto_data_comparable import DTODataComparable


class BusinessDTO(BaseModel, DTODataComparable):
    id: int
    name: str
    facebook_url: Optional[str]

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __eq__(self, other: Any) -> bool:
        return self._data_eq(other) and self.id == other.id

    def _data_hash(self) -> int:
        return self.name.__hash__()

    def _data_eq(self, other: Any) -> bool:
        if not isinstance(other, BusinessDTO):
            return False
        return (self.name == other.name and
                self.facebook_url == other.facebook_url)

    @classmethod
    def from_entity(cls, entity: Business) -> "BusinessDTO":
        return cls(id=entity.id,
                   name=entity.name,
                   facebook_url=entity.facebook_url)


class BusinessesGetAllResponse(BaseModel):
    businesses: FrozenSet[BusinessDTO]

    def __hash__(self) -> int:
        return self.users.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BusinessesGetAllResponse):
            return False
        return self.businesses == other.businesses


class BusinessAddForm(BaseModel):
    name: str
    facebook_url: Optional[str]


class BusinessOperationSuccessResponse(BaseModel):
    business: BusinessDTO

    def __hash__(self) -> int:
        return self.business.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BusinessOperationSuccessResponse):
            return False
        return self.business == other.business

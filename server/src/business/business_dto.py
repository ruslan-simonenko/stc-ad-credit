from typing import Any, Optional

from pydantic import BaseModel

from src.business.business_types import BusinessRegistrationType
from src.persistence.schema.business import Business
from src.utils.dto_data_comparable import DTODataComparable


class BusinessDTO(BaseModel, DTODataComparable):
    id: int
    name: str
    registration_type: BusinessRegistrationType
    registration_number: str
    email: Optional[str]
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
                self.registration_type == other.registration_type and
                self.registration_number == other.registration_number and
                self.email == other.email and
                self.facebook_url == other.facebook_url)

    @classmethod
    def from_entity(cls, entity: Business) -> "BusinessDTO":
        return cls(id=entity.id,
                   name=entity.name,
                   registration_type=BusinessRegistrationType(entity.registration_type),
                   registration_number=entity.registration_number,
                   email=entity.email,
                   facebook_url=entity.facebook_url)


class BusinessDTOPublic(BaseModel, DTODataComparable):
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
        if not isinstance(other, BusinessDTOPublic):
            return False
        return (self.name == other.name and
                self.facebook_url == other.facebook_url)

    @classmethod
    def from_entity(cls, entity: Business) -> "BusinessDTOPublic":
        return cls(id=entity.id,
                   name=entity.name,
                   facebook_url=entity.facebook_url)


class BusinessAddForm(BaseModel):
    name: str
    registration_type: BusinessRegistrationType
    registration_number: str
    email: Optional[str]
    facebook_url: Optional[str]

from datetime import datetime
from typing import Any, FrozenSet

from pydantic import BaseModel

from src.persistence.schema.ad_record import AdRecord
from src.utils.dto_data_comparable import DTODataComparable


class AdRecordDTO(BaseModel, DTODataComparable):
    id: int
    business_id: int
    ad_post_url: str
    creator_id: int
    created_at: datetime

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __eq__(self, other: Any) -> bool:
        return self._data_eq(other) and (
                self.id == other.id)

    def _data_hash(self) -> int:
        return self.ad_post_url.__hash__()

    def _data_eq(self, other: Any) -> bool:
        if not isinstance(other, AdRecordDTO):
            return False
        return (self.business_id == other.business_id and
                self.ad_post_url == other.ad_post_url and
                self.creator_id == other.creator_id)

    @classmethod
    def from_entity(cls, entity: AdRecord) -> "AdRecordDTO":
        return cls(id=entity.id,
                   business_id=entity.business_id,
                   ad_post_url=entity.ad_post_url,
                   creator_id=entity.created_by,
                   created_at=entity.created_at)


class AdRecordsDTO(BaseModel):
    records: FrozenSet[AdRecordDTO]

    def __hash__(self) -> int:
        return self.records.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AdRecordsDTO):
            return False
        return self.records == other.records


class AdRecordAddFormDTO(BaseModel):
    business_id: int
    ad_post_url: str


class ErrorResponse(BaseModel):
    message: str

    def __hash__(self) -> int:
        return self.message.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ErrorResponse):
            return False
        return self.message == other.message

from datetime import date
from typing import FrozenSet, Any

from pydantic import BaseModel

from src.persistence.schema.carbon_audit import CarbonAudit
from src.utils.dto_data_comparable import DTODataComparable


class CarbonAuditDTO(BaseModel, DTODataComparable):
    id: int
    business_id: int
    creator_id: int
    score: int
    report_date: date
    report_url: str

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __eq__(self, other: Any) -> bool:
        return self._data_eq(other) and (
                self.id == other.id and
                self.business_id == other.business_id and
                self.creator_id == other.creator_id)

    def _data_hash(self) -> int:
        return self.report_url.__hash__()

    def _data_eq(self, other: Any) -> bool:
        if not isinstance(other, CarbonAuditDTO):
            return False
        return (self.score == other.score and
                self.report_date == other.report_date and
                self.report_url == other.report_url)

    @classmethod
    def from_entity(cls, entity: CarbonAudit) -> "CarbonAuditDTO":
        return cls(id=entity.id,
                   business_id=entity.business_id,
                   creator_id=entity.created_by,
                   score=entity.score,
                   report_date=entity.report_date,
                   report_url=entity.report_url)


class CarbonAuditsGetResponse(BaseModel):
    audits: FrozenSet[CarbonAuditDTO]

    def __hash__(self) -> int:
        return self.users.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CarbonAuditsGetResponse):
            return False
        return self.audits == other.audits

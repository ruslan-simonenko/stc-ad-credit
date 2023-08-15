from typing import Optional, Dict

from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating
from src.persistence.schema.carbon_audit import CarbonAudit


class CarbonAuditRatingService:
    @staticmethod
    def get_for_audit(audit: Optional[CarbonAudit]) -> CarbonAuditRating:
        if audit is None:
            return CarbonAuditRating.UNKNOWN
        for rating in [CarbonAuditRating.HIGH, CarbonAuditRating.MEDIUM]:
            if audit.score >= CARBON_RATING_MIN_SCORE[rating]:
                return rating
        return CarbonAuditRating.LOW


CARBON_RATING_MIN_SCORE: Dict[CarbonAuditRating, int] = {
    CarbonAuditRating.MEDIUM: 50,
    CarbonAuditRating.HIGH: 70,
}

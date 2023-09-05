from typing import Optional, Dict

from src.business.business_service import BusinessService
from src.business.business_types import BusinessRegistrationType
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating
from src.persistence.schema.business import Business
from src.persistence.schema.carbon_audit import CarbonAudit


class CarbonAuditRatingService:

    @staticmethod
    def get_for_business(business_id: int) -> CarbonAuditRating:
        business = BusinessService.get_by_id_or_throw(business_id)
        latest_audit = CarbonAuditService.get_latest_for_business(business_id)
        return CarbonAuditRatingService.get_for_business_and_audit(business, latest_audit)

    @staticmethod
    def get_for_business_and_audit(business: Business, audit: Optional[CarbonAudit]) -> CarbonAuditRating:
        if audit is None:
            if business.registration_type == BusinessRegistrationType.KNOWN:
                return CarbonAuditRating.UNKNOWN
            else:
                return CarbonAuditRating.LOW
        for rating in [CarbonAuditRating.HIGH, CarbonAuditRating.MEDIUM]:
            if audit.score >= CARBON_RATING_MIN_SCORE[rating]:
                return rating
        return CarbonAuditRating.LOW


CARBON_RATING_MIN_SCORE: Dict[CarbonAuditRating, int] = {
    CarbonAuditRating.MEDIUM: 50,
    CarbonAuditRating.HIGH: 70,
}

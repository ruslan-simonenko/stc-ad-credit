from src.ad_credit.ad_strategy import AD_ALLOWANCE, CarbonAuditRating, CARBON_RATING_MIN_SCORE
from src.carbon_audit.carbon_audit_service import CarbonAuditService


class AdCreditService:

    @staticmethod
    def get_allowance(business_id: int) -> int:
        rating = AdCreditService._get_rating(business_id)
        return AD_ALLOWANCE[rating]

    @staticmethod
    def _get_rating(business_id: int) -> CarbonAuditRating:
        latest_audit = CarbonAuditService.get_latest(business_id)
        if latest_audit is None:
            return CarbonAuditRating.UNKNOWN
        for rating in [CarbonAuditRating.HIGH, CarbonAuditRating.MEDIUM]:
            if latest_audit.score >= CARBON_RATING_MIN_SCORE[rating]:
                return rating
        return CarbonAuditRating.LOW

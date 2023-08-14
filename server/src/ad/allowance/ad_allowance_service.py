from src.ad.strategy.ad_strategy import AD_ALLOWANCE, CarbonAuditRating, CARBON_RATING_MIN_SCORE, \
    AD_RATE_LIMIT_WINDOW_DURATION
from src.ad.record.ad_record_service import AdRecordService
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.utils.clock import Clock


class AdAllowanceService:

    @staticmethod
    def get_allowance(business_id: int) -> int:
        rating = AdAllowanceService._get_rating(business_id)
        return AD_ALLOWANCE[rating]

    @staticmethod
    def get_used_allowance(business_id: int) -> int:
        return AdRecordService.get_count_for_business_since_date(
            business_id,
            since=Clock.now() - AD_RATE_LIMIT_WINDOW_DURATION)

    @staticmethod
    def get_remaining_allowance(business_id: int) -> int:
        return AdAllowanceService.get_allowance(business_id) - AdAllowanceService.get_used_allowance(business_id)

    @staticmethod
    def _get_rating(business_id: int) -> CarbonAuditRating:
        latest_audit = CarbonAuditService.get_latest(business_id)
        if latest_audit is None:
            return CarbonAuditRating.UNKNOWN
        for rating in [CarbonAuditRating.HIGH, CarbonAuditRating.MEDIUM]:
            if latest_audit.score >= CARBON_RATING_MIN_SCORE[rating]:
                return rating
        return CarbonAuditRating.LOW

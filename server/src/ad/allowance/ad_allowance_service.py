from typing import Dict, Optional

from src.ad.allowance.ad_allowance_types import AdAllowance
from src.ad.record.ad_record_service import AdRecordService
from src.ad.strategy.ad_strategy import AD_ALLOWANCE, CARBON_RATING_MIN_SCORE, \
    AD_RATE_LIMIT_WINDOW_DURATION
from src.carbon_audit.carbon_audit_types import CarbonAuditRating
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.persistence.schema.carbon_audit import CarbonAudit
from src.utils.clock import Clock


class AdAllowanceService:

    @staticmethod
    def get_allowance(business_id: int) -> int:
        rating = AdAllowanceService._get_rating_for_business(business_id)
        return AD_ALLOWANCE[rating]

    @staticmethod
    def get_used_allowance(business_id: int) -> int:
        return AdRecordService.get_count_for_business_since_date(
            business_id,
            since=AdAllowanceService._get_rate_limit_window_start())

    @staticmethod
    def get_remaining_allowance(business_id: int) -> int:
        return AdAllowanceService.get_allowance(business_id) - AdAllowanceService.get_used_allowance(business_id)

    @staticmethod
    def get_for_all_businesses() -> Dict[int, AdAllowance]:
        business_id_to_allowance = {
            audit.business_id: AD_ALLOWANCE[AdAllowanceService._get_rating_for_carbon_audit(audit)]
            for audit in CarbonAuditService.get_latest()}
        business_id_to_used_allowance = AdRecordService.get_count_for_all_businesses_since_date(
            AdAllowanceService._get_rate_limit_window_start())
        all_business_ids = set(business_id_to_used_allowance)
        return {business_id: AdAllowance(
            full=business_id_to_allowance.get(business_id, AD_ALLOWANCE[CarbonAuditRating.UNKNOWN]),
            used=business_id_to_used_allowance.get(business_id, 0)
        ) for business_id in all_business_ids}

    @staticmethod
    def _get_rating_for_business(business_id: int) -> CarbonAuditRating:
        latest_audit = CarbonAuditService.get_latest_for_business(business_id)
        return AdAllowanceService._get_rating_for_carbon_audit(latest_audit)

    @staticmethod
    def _get_rating_for_carbon_audit(audit: Optional[CarbonAudit]) -> CarbonAuditRating:
        if audit is None:
            return CarbonAuditRating.UNKNOWN
        for rating in [CarbonAuditRating.HIGH, CarbonAuditRating.MEDIUM]:
            if audit.score >= CARBON_RATING_MIN_SCORE[rating]:
                return rating
        return CarbonAuditRating.LOW

    @staticmethod
    def _get_rate_limit_window_start():
        return Clock.now() - AD_RATE_LIMIT_WINDOW_DURATION

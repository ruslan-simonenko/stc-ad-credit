from typing import Dict

from src.ad.allowance.ad_allowance_types import AdAllowance
from src.ad.record.ad_record_service import AdRecordService
from src.ad.strategy.ad_strategy import AD_ALLOWANCE, AD_RATE_LIMIT_WINDOW_DURATION
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.carbon_audit.rating.carbon_audit_rating_service import CarbonAuditRatingService
from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating
from src.utils.clock import Clock


class AdAllowanceService:

    @staticmethod
    def get_for_business(business_id) -> AdAllowance:
        full = AD_ALLOWANCE[CarbonAuditRatingService.get_for_business(business_id)]
        used = AdRecordService.get_count_for_business_since_date(
            business_id,
            since=AdAllowanceService._get_rate_limit_window_start())
        return AdAllowance(full=full, used=used)

    @staticmethod
    def get_for_all_businesses() -> Dict[int, AdAllowance]:
        business_id_to_allowance = {
            audit.business_id: AD_ALLOWANCE[CarbonAuditRatingService.get_for_audit(audit)]
            for audit in CarbonAuditService.get_latest()}
        business_id_to_used_allowance = AdRecordService.get_count_for_all_businesses_since_date(
            AdAllowanceService._get_rate_limit_window_start())
        all_business_ids = set(business_id_to_used_allowance)
        return {business_id: AdAllowance(
            full=business_id_to_allowance.get(business_id, AD_ALLOWANCE[CarbonAuditRating.UNKNOWN]),
            used=business_id_to_used_allowance.get(business_id, 0)
        ) for business_id in all_business_ids}

    @staticmethod
    def _get_rate_limit_window_start():
        return Clock.now() - AD_RATE_LIMIT_WINDOW_DURATION

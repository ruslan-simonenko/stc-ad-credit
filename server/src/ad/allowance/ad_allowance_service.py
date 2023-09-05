from typing import Dict

from src.ad.allowance.ad_allowance_types import AdAllowance
from src.ad.record.ad_record_service import AdRecordService
from src.ad.strategy.ad_strategy import AD_ALLOWANCE, AD_RATE_LIMIT_WINDOW_DURATION
from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.carbon_audit.rating.carbon_audit_rating_service import CarbonAuditRatingService
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
        businesses = {business.id: business for business in BusinessService.get_all()}
        all_business_ids = set(businesses.keys())
        business_id_to_latest_audit = {audit.business_id: audit for audit in CarbonAuditService.get_latest()}
        business_id_to_allowance = {
            business_id: AD_ALLOWANCE[CarbonAuditRatingService.get_for_business_and_audit(
                businesses[business_id], business_id_to_latest_audit.get(business_id, None)
            )]
            for business_id in all_business_ids}
        business_id_to_used_allowance = AdRecordService.get_count_for_all_businesses_since_date(
            AdAllowanceService._get_rate_limit_window_start())
        return {business_id: AdAllowance(
            full=business_id_to_allowance.get(business_id),
            used=business_id_to_used_allowance.get(business_id, 0)
        ) for business_id in all_business_ids}

    @staticmethod
    def _get_rate_limit_window_start():
        return Clock.now() - AD_RATE_LIMIT_WINDOW_DURATION

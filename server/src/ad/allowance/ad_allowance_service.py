from datetime import datetime
from typing import Dict, Optional

from src.ad.allowance.ad_allowance_types import AdAllowance
from src.ad.record.ad_record_service import AdRecordService
from src.ad.strategy.ad_strategy import AD_ALLOWANCE, AD_RATE_LIMIT_WINDOW_DURATION
from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.carbon_audit.rating.carbon_audit_rating_service import CarbonAuditRatingService
from src.persistence.schema.business import Business
from src.persistence.schema.carbon_audit import CarbonAudit
from src.utils.clock import Clock


class AdAllowanceService:

    @staticmethod
    def get_for_business(business_id) -> AdAllowance:
        business = BusinessService.get_by_id_or_throw(business_id)
        latest_audit = CarbonAuditService.get_latest_for_business(business_id)

        window_start = AdAllowanceService._get_rate_limit_window_start(business, latest_audit)
        full = AD_ALLOWANCE[CarbonAuditRatingService.get_for_business_and_audit(business, latest_audit)]
        used = AdRecordService.get_count_for_business_since_date(business_id, since=window_start)
        return AdAllowance(window_start=window_start, full=full, used=used)

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
        business_id_to_window_start = {
            business_id: AdAllowanceService._get_rate_limit_window_start(
                businesses[business_id], business_id_to_latest_audit.get(business_id, None)
            )
            for business_id in all_business_ids
        }
        business_id_to_used_allowance = AdRecordService.get_count_for_all_businesses_since_dates(
            business_id_to_window_start)
        return {business_id: AdAllowance(
            window_start=business_id_to_window_start.get(business_id),
            full=business_id_to_allowance.get(business_id),
            used=business_id_to_used_allowance.get(business_id)
        ) for business_id in all_business_ids}

    @staticmethod
    def _get_rate_limit_window_start(business: Business, latest_audit: Optional[CarbonAudit]):
        if latest_audit is None:
            initial_window_start = business.created_at
        else:
            initial_window_start = datetime.combine(latest_audit.report_date, datetime.min.time())
        full_windows_passed = (Clock.now() - initial_window_start) // AD_RATE_LIMIT_WINDOW_DURATION
        return initial_window_start + full_windows_passed * AD_RATE_LIMIT_WINDOW_DURATION

from datetime import datetime, timedelta
from typing import Optional
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.ad.allowance import ad_allowance_service
from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.ad.allowance.ad_allowance_types import AdAllowance
from src.ad.record.ad_record_service import AdRecordService
from src.ad.strategy.ad_strategy import AD_ALLOWANCE
from src.business.business_service import BusinessService
from src.business.business_types import BusinessRegistrationType
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.carbon_audit.rating.carbon_audit_rating_service import CARBON_RATING_MIN_SCORE
from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating
from src.persistence.schema.business import Business
from src.persistence.schema.carbon_audit import CarbonAudit
from src.utils.clock import Clock

BUSINESS_ID = 10


class TestAdAllowanceService:

    def test_get_for_all_businesses(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(BusinessService, 'get_all', lambda: [
            business_mock(business_id=1, reg_type=BusinessRegistrationType.VAT),
            business_mock(business_id=2, reg_type=BusinessRegistrationType.CRN),
            business_mock(business_id=3, reg_type=BusinessRegistrationType.NI),
            business_mock(business_id=4, reg_type=BusinessRegistrationType.VAT),
            business_mock(business_id=5, reg_type=BusinessRegistrationType.KNOWN),
        ])
        monkeypatch.setattr(CarbonAuditService, 'get_latest', lambda: [
            carbon_audit_mock(business_id=1, score=CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH]),
            carbon_audit_mock(business_id=2, score=CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM]),
            carbon_audit_mock(business_id=3, score=0),
        ])
        monkeypatch.setattr(AdRecordService, 'get_count_for_all_businesses_since_date', lambda since: {
            1: 6,
            2: 7,
            3: 2,
            4: 1,
            5: 0})
        actual_result = AdAllowanceService.get_for_all_businesses()
        assert actual_result == {
            1: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.HIGH], used=6),
            2: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.MEDIUM], used=7),
            3: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.LOW], used=2),
            4: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.LOW], used=1),
            5: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.UNKNOWN], used=0),
        }

    @pytest.mark.parametrize('biz_created_days_ago, audit_made_days_ago, expected_window_start_days_ago', [
        (3, None, 3),
        (9, None, 9),
        (10, None, 0),
        (15, None, 5),
        (107, None, 7),
        (107, 33, 3),
        (57, 55, 5),
        (1399, 350, 0),
    ])
    def test_get_rate_limit_window_start_NEW(self, monkeypatch: MonkeyPatch,
                                             biz_created_days_ago,
                                             audit_made_days_ago: Optional[int],
                                             expected_window_start_days_ago: int):
        current_time = datetime.utcnow()

        business = Mock()
        business.created_at = current_time - timedelta(days=biz_created_days_ago)

        if audit_made_days_ago is None:
            audit = None
        else:
            audit = Mock()
            audit.report_date = current_time - timedelta(days=audit_made_days_ago)

        monkeypatch.setattr(ad_allowance_service, 'AD_RATE_LIMIT_WINDOW_DURATION', timedelta(days=10))
        monkeypatch.setattr(Clock, 'now', lambda: current_time)

        actual_window_start = AdAllowanceService._get_rate_limit_window_start_NEW(business, audit)
        expected_window_start = current_time - timedelta(days=expected_window_start_days_ago)
        assert abs(actual_window_start - expected_window_start) < timedelta(hours=1)


def carbon_audit_mock(business_id: int = None, score: int = None) -> CarbonAudit:
    audit = Mock()
    audit.business_id = business_id
    audit.score = score
    return audit


def business_mock(business_id: int, reg_type: BusinessRegistrationType) -> Business:
    business = Mock()
    business.id = business_id
    business.registration_type = reg_type
    return business

from typing import Optional
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.ad.allowance.ad_allowance_types import AdAllowance
from src.ad.record.ad_record_service import AdRecordService
from src.ad.strategy.ad_strategy import AD_ALLOWANCE, CARBON_RATING_MIN_SCORE
from src.carbon_audit.carbon_audit_types import CarbonAuditRating
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.persistence.schema.carbon_audit import CarbonAudit

BUSINESS_ID = 10


class TestAdAllowanceService:

    @pytest.mark.parametrize('latest_audit_score, expected_rating', [
        # No audits
        (None, CarbonAuditRating.UNKNOWN),
        # Single audit
        (0, CarbonAuditRating.LOW),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM] - 1, CarbonAuditRating.LOW),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM], CarbonAuditRating.MEDIUM),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] - 1, CarbonAuditRating.MEDIUM),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH], CarbonAuditRating.HIGH),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] + 50, CarbonAuditRating.HIGH),
    ])
    def test_get_allowance(self,
                           monkeypatch: MonkeyPatch,
                           latest_audit_score: Optional[int],
                           expected_rating: CarbonAuditRating):
        def mock_get_latest_audit(business_id: int) -> Optional[CarbonAudit]:
            if business_id != BUSINESS_ID:
                return None
            if latest_audit_score is None:
                return None
            return carbon_audit_mock(score=latest_audit_score)

        monkeypatch.setattr(CarbonAuditService, 'get_latest_for_business', mock_get_latest_audit)
        assert AdAllowanceService.get_allowance(BUSINESS_ID) == AD_ALLOWANCE[expected_rating]

    def test_get_for_all_businesses(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(CarbonAuditService, 'get_latest', lambda: [
            carbon_audit_mock(business_id=1, score=CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH]),
            carbon_audit_mock(business_id=2, score=CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM]),
            carbon_audit_mock(business_id=3, score=0),
        ])
        monkeypatch.setattr(AdRecordService, 'get_count_for_all_businesses_since_date', lambda since: {
            1: 6,
            2: 7,
            3: 2,
            4: 1})
        actual_result = AdAllowanceService.get_for_all_businesses()
        assert actual_result == {
            1: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.HIGH], used=6),
            2: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.MEDIUM], used=7),
            3: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.LOW], used=2),
            4: AdAllowance(full=AD_ALLOWANCE[CarbonAuditRating.UNKNOWN], used=1),
        }


def carbon_audit_mock(business_id: int = None, score: int = None) -> CarbonAudit:
    audit = Mock()
    audit.business_id = business_id
    audit.score = score
    return audit

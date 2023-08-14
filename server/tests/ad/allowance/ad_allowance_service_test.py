from typing import Optional
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.ad.strategy.ad_strategy import AD_ALLOWANCE, CarbonAuditRating, CARBON_RATING_MIN_SCORE
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
            audit = Mock()
            audit.score = latest_audit_score
            return audit

        monkeypatch.setattr(CarbonAuditService, 'get_latest', mock_get_latest_audit)
        assert AdAllowanceService.get_allowance(BUSINESS_ID) == AD_ALLOWANCE[expected_rating]

from typing import Optional
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.carbon_audit.rating.carbon_audit_rating_service import CARBON_RATING_MIN_SCORE, CarbonAuditRatingService
from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating
from src.persistence.schema.carbon_audit import CarbonAudit


class TestCarbonAuditRatingService:

    @pytest.mark.parametrize('latest_audit_score, expected_rating', [
        (None, CarbonAuditRating.UNKNOWN),
        (0, CarbonAuditRating.LOW),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM] - 1, CarbonAuditRating.LOW),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM], CarbonAuditRating.MEDIUM),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] - 1, CarbonAuditRating.MEDIUM),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH], CarbonAuditRating.HIGH),
        (CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] + 50, CarbonAuditRating.HIGH),
    ])
    def test_get_for_audit(self,
                           monkeypatch: MonkeyPatch,
                           latest_audit_score: Optional[int],
                           expected_rating: CarbonAuditRating):
        if latest_audit_score is None:
            audit = None
        else:
            audit = Mock()
            audit.score = latest_audit_score
        assert CarbonAuditRatingService.get_for_audit(audit) == expected_rating


def carbon_audit_mock(score: int = None) -> CarbonAudit:
    audit = Mock()
    audit.score = score
    return audit

from typing import Optional
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.business.business_service import BusinessService
from src.business.business_types import BusinessRegistrationType
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.carbon_audit.rating.carbon_audit_rating_service import CARBON_RATING_MIN_SCORE, CarbonAuditRatingService
from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating
from src.persistence.schema.business import Business
from src.persistence.schema.carbon_audit import CarbonAudit


class TestCarbonAuditRatingService:

    @pytest.mark.parametrize('business_reg_type, latest_audit_score, expected_rating', [
        # No audit
        (BusinessRegistrationType.KNOWN, None, CarbonAuditRating.UNKNOWN),
        (BusinessRegistrationType.VAT, None, CarbonAuditRating.LOW),
        # Audit-based
        (BusinessRegistrationType.VAT, 0, CarbonAuditRating.LOW),
        (BusinessRegistrationType.VAT, CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM] - 1, CarbonAuditRating.LOW),
        (BusinessRegistrationType.NI, CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM], CarbonAuditRating.MEDIUM),
        (BusinessRegistrationType.NI, CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] - 1, CarbonAuditRating.MEDIUM),
        (BusinessRegistrationType.CRN, CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH], CarbonAuditRating.HIGH),
        (BusinessRegistrationType.CRN, CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] + 50, CarbonAuditRating.HIGH),
    ])
    def test_get_for_business_and_audit(self,
                                        monkeypatch: MonkeyPatch,
                                        business_reg_type: BusinessRegistrationType,
                                        latest_audit_score: Optional[int],
                                        expected_rating: CarbonAuditRating):
        business = Mock()
        business.registration_type = business_reg_type
        if latest_audit_score is None:
            audit = None
        else:
            audit = Mock()
            audit.score = latest_audit_score
        assert CarbonAuditRatingService.get_for_business_and_audit(business, audit) == expected_rating

    def test_get_for_business(self, monkeypatch: MonkeyPatch):
        BUSINESS_ID = 167
        audit = Mock()
        business = Mock()

        def mock_get_business(business_id: int) -> Business:
            assert business_id == BUSINESS_ID
            return business

        def mock_get_latest_audit(business_id: int) -> CarbonAudit:
            assert business_id == BUSINESS_ID
            return audit

        def mock_get_for_business_and_audit(business_: Business, audit_: CarbonAudit) -> CarbonAuditRating:
            assert audit_ is audit
            assert business_ is business
            return CarbonAuditRating.MEDIUM

        monkeypatch.setattr(BusinessService, 'get_by_id_or_throw', mock_get_business)
        monkeypatch.setattr(CarbonAuditService, 'get_latest_for_business', mock_get_latest_audit)
        monkeypatch.setattr(CarbonAuditRatingService, 'get_for_business_and_audit', mock_get_for_business_and_audit)
        assert CarbonAuditRatingService.get_for_business(BUSINESS_ID) == CarbonAuditRating.MEDIUM


def carbon_audit_mock(score: int = None) -> CarbonAudit:
    audit = Mock()
    audit.score = score
    return audit

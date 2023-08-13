from datetime import datetime
from typing import List

import pytest

from app import app
from src.ad_credit.ad_credit_service import AdCreditService
from src.ad_credit.ad_strategy import AD_ALLOWANCE, CarbonAuditRating, CARBON_RATING_MIN_SCORE
from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.persistence.schema.business import Business
from src.persistence.schema.user import User
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest


class TestAdCreditService(DatabaseTest):
    @pytest.fixture(autouse=True)
    def setup_app_context(self):
        with app.app_context():
            yield

    @pytest.fixture
    def user_admin(self, setup_app_context) -> User:
        return UserService.add_user('admin@stc.com', [UserRole.ADMIN])

    @pytest.fixture
    def user_carbon_auditor(self, setup_app_context) -> User:
        return UserService.add_user('carbon-auditor@stc.com', [UserRole.CARBON_AUDITOR])

    @pytest.fixture
    def business(self, user_admin) -> Business:
        return BusinessService.add(name='Test Business', facebook_url=None, creator_id=user_admin.id)

    @pytest.mark.parametrize('audit_scores, expected_rating', [
        # No audits
        ([], CarbonAuditRating.UNKNOWN),
        # Single audit
        ([0], CarbonAuditRating.LOW),
        ([CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM] - 1], CarbonAuditRating.LOW),
        ([CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM]], CarbonAuditRating.MEDIUM),
        ([CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] - 1], CarbonAuditRating.MEDIUM),
        ([CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH]], CarbonAuditRating.HIGH),
        ([CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH] + 50], CarbonAuditRating.HIGH),
        # Uses latest
        ([100, 80, 70, 90, CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM] - 1], CarbonAuditRating.LOW),
        ([0, 10, 0, 20, CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH]], CarbonAuditRating.HIGH),
    ])
    def test_get_allowance(self,
                           user_carbon_auditor: User,
                           business: Business,
                           audit_scores: List[int],
                           expected_rating: CarbonAuditRating):
        for audit_score in audit_scores:
            CarbonAuditService.add(
                business.id,
                audit_score,
                report_date=datetime.utcnow(),
                report_url='https://reports.stc.org/105',
                creator_id=user_carbon_auditor.id)
        assert AdCreditService.get_allowance(business.id) == AD_ALLOWANCE[expected_rating]

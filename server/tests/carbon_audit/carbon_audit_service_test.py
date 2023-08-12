from datetime import datetime, timedelta, date
from typing import List

import pytest

from app import app
from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.persistence.schema.business import Business
from src.persistence.schema.carbon_audit import CarbonAudit
from src.persistence.schema.user import User
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest


class TestCarbonAuditService(DatabaseTest):
    AUDIT_REPORT_URL = 'https://reports.seethroughcarbon.org/report-19365'
    AUDIT_SCORE = 85

    @pytest.fixture(autouse=True)
    def setup_app_context(self):
        with app.app_context():
            yield

    @pytest.fixture(autouse=True)
    def current_user(self, setup_app_context) -> User:
        return UserService.add_user('test@gmail.com', [UserRole.ADMIN])

    @pytest.fixture
    def business(self, current_user) -> Business:
        return BusinessService.add(name='Test Business', facebook_url=None, creator_id=current_user.id)

    def test_add_carbon_audit(self, current_user: User, business: Business):
        carbon_audit = CarbonAuditService.add(
            business_id=business.id,
            score=self.AUDIT_SCORE,
            report_date=date.today(),
            report_url=self.AUDIT_REPORT_URL,
            creator_id=current_user.id
        )
        assert carbon_audit.business_id == business.id
        assert carbon_audit.score == self.AUDIT_SCORE
        assert carbon_audit.report_date == date.today()
        assert carbon_audit.report_url == self.AUDIT_REPORT_URL
        assert datetime.utcnow() - carbon_audit.created_at < timedelta(minutes=1)

    def test_add_multiple_audits_for_a_single_business(self, current_user: User, business: Business):
        for score, report_date in [
            (70, date.today() - timedelta(days=60)),
            (60, date.today() - timedelta(days=30)),
            (90, date.today())
        ]:
            carbon_audit = CarbonAuditService.add(
                business_id=business.id,
                score=score,
                report_date=report_date,
                report_url=self.AUDIT_REPORT_URL,
                creator_id=current_user.id
            )
            assert carbon_audit.business_id == business.id
            assert carbon_audit.score == score
            assert carbon_audit.report_date == report_date
            assert carbon_audit.report_url == self.AUDIT_REPORT_URL
            assert datetime.utcnow() - business.created_at < timedelta(minutes=1)

    class TestGetLatestCreatedByUser:
        @pytest.fixture()
        def carbon_audits(self, current_user, business) -> List[CarbonAudit]:
            return [CarbonAuditService.add(
                business_id=business.id,
                score=score,
                report_date=report_date,
                report_url=TestCarbonAuditService.AUDIT_REPORT_URL + str(index),
                creator_id=current_user.id
            ) for index, (score, report_date) in enumerate([
                (70, date.today() - timedelta(days=60)),
                (60, date.today() - timedelta(days=30)),
                (90, date.today())
            ])]

        def test_get_all(self, carbon_audits: List[CarbonAudit]):
            actual_carbon_audits = CarbonAuditService.get_all()
            assert actual_carbon_audits == list(reversed(carbon_audits))

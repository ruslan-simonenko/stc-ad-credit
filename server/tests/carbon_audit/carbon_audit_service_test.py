from datetime import datetime, timedelta, date

import pytest

from app import app
from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_service import CarbonAuditService
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

    def test_add_carbon_audit(self, current_user: User):
        business = BusinessService.add(name='Test Business', facebook_url=None, creator_id=current_user.id)
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
        assert datetime.utcnow() - business.created_at < timedelta(minutes=1)

    def test_add_multiple_audits_for_a_single_business(self, current_user: User):
        business = BusinessService.add(name='Test Business', facebook_url=None, creator_id=current_user.id)
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



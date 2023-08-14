from datetime import datetime, timedelta, date
from typing import List

import pytest

from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.persistence.schema.business import Business
from src.persistence.schema.carbon_audit import CarbonAudit
from tests.app_fixtures import AutoAppContextFixture
from tests.business.business_fixtures import BusinessFixtures
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures


class TestCarbonAuditService(DatabaseTest, AutoAppContextFixture, BusinessFixtures, UserFixtures):
    AUDIT_REPORT_URL = 'https://reports.seethroughcarbon.org/report-19365'
    AUDIT_SCORE = 85

    def test_add_carbon_audit(self, users, business: Business):
        carbon_audit = CarbonAuditService.add(
            business_id=business.id,
            score=self.AUDIT_SCORE,
            report_date=date.today(),
            report_url=self.AUDIT_REPORT_URL,
            creator_id=users.admin.id
        )
        assert carbon_audit.business_id == business.id
        assert carbon_audit.score == self.AUDIT_SCORE
        assert carbon_audit.report_date == date.today()
        assert carbon_audit.report_url == self.AUDIT_REPORT_URL
        assert datetime.utcnow() - carbon_audit.created_at < timedelta(minutes=1)

    def test_add_multiple_audits_for_a_single_business(self, users, business: Business):
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
                creator_id=users.admin.id
            )
            assert carbon_audit.business_id == business.id
            assert carbon_audit.score == score
            assert carbon_audit.report_date == report_date
            assert carbon_audit.report_url == self.AUDIT_REPORT_URL
            assert datetime.utcnow() - business.created_at < timedelta(minutes=1)

    class TestGet:
        @pytest.fixture()
        def carbon_audits(self, users, business) -> List[CarbonAudit]:
            return [CarbonAuditService.add(
                business_id=business.id,
                score=score,
                report_date=report_date,
                report_url=TestCarbonAuditService.AUDIT_REPORT_URL + str(index),
                creator_id=users.admin.id
            ) for index, (score, report_date) in enumerate([
                (70, date.today() - timedelta(days=60)),
                (60, date.today() - timedelta(days=30)),
                (90, date.today())
            ])]

        def test_get_all(self, carbon_audits: List[CarbonAudit]):
            actual_carbon_audits = CarbonAuditService.get_all()
            assert actual_carbon_audits == list(reversed(carbon_audits))

        def test_get_latest_for_business__returns_latest(self, carbon_audits: List[CarbonAudit], business: Business):
            actual_carbon_audit = CarbonAuditService.get_latest_for_business(business.id)
            assert actual_carbon_audit == carbon_audits[-1]

        def test_get_latest_for_business__none_available(self, business):
            actual_carbon_audit = CarbonAuditService.get_latest_for_business(business.id)
            assert actual_carbon_audit is None

        def test_get_latest_for_all_businesses(self, businesses, users):
            expected_latest_audits = []
            for business_id, audit_scores in {
                businesses.apple.id: [30, 60, 90],
                businesses.banana.id: [10, 5],
                businesses.pear.id: []
            }.items():
                for index, audit_score in enumerate(audit_scores):
                    added_audit = CarbonAuditService.add(
                        business_id=business_id,
                        score=audit_score,
                        report_date=date.today() + timedelta(days=index - 100),
                        report_url=TestCarbonAuditService.AUDIT_REPORT_URL,
                        creator_id=users.carbon_auditor.id
                    )
                    if index == len(audit_scores) - 1:
                        expected_latest_audits.append(added_audit)
            actual_latest_audits = CarbonAuditService.get_latest()
            assert set(actual_latest_audits) == set(expected_latest_audits)

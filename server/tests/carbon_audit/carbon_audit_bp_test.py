from datetime import datetime, timedelta

from flask.testing import FlaskClient

from src.carbon_audit.carbon_audit_dto import CarbonAuditDTO, CarbonAuditAddForm
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.utils.dto import ResponseWithObjects, ResponseWithObject
from tests.app_fixtures import AutoAppContextFixture
from tests.auth.auth_fixtures import AuthFixtures
from tests.business.business_test_utils import BusinessTestUtils
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures
from tests.utils.dto_comparison_utils import patched_dto_for_comparison


class TestCarbonAuditEndpoint(DatabaseTest, AuthFixtures, UserFixtures, AutoAppContextFixture):
    class TestAdd:
        def test_add_audit(self, client: FlaskClient, users, access_headers_for):
            business = BusinessTestUtils.add_business(users.business_manager)
            form = CarbonAuditAddForm(
                business_id=business.id,
                score=50,
                report_date=datetime.utcnow().date(),
                report_url='https://reports.stc.org/10',
            )

            response = client.post('/carbon_audits/', json=form, headers=access_headers_for(users.carbon_auditor))

            assert response.status_code == 200
            with patched_dto_for_comparison(CarbonAuditDTO):
                actual_data = ResponseWithObject[CarbonAuditDTO].model_validate(response.json)
                expected_audit = CarbonAuditDTO(
                    id=0,
                    business_id=business.id,
                    creator_id=users.admin.id,
                    score=50,
                    report_date=datetime.utcnow().date(),
                    report_url='https://reports.stc.org/10',
                )
                assert actual_data.object == expected_audit

    class TestGetAll:
        def test_get_audits(self, client: FlaskClient, users, access_headers_for):
            business = BusinessTestUtils.add_business(users.business_manager)
            audits = [CarbonAuditService.add(
                business_id=business.id,
                score=score,
                report_date=report_date,
                report_url='https://reports.stc.org/10',
                creator_id=users.carbon_auditor.id,
            ) for score, report_date in [
                (84, datetime.utcnow().date() - timedelta(days=90)),
                (91, datetime.utcnow().date() - timedelta(days=60)),
                (85, datetime.utcnow().date() - timedelta(days=30)),
                (66, datetime.utcnow().date()),
            ]]

            response = client.get('/carbon_audits/', headers=access_headers_for(users.carbon_auditor))

            assert response.status_code == 200
            with patched_dto_for_comparison(CarbonAuditDTO):
                actual_data = ResponseWithObjects[CarbonAuditDTO].model_validate(response.json)
                expected_data = ResponseWithObjects[CarbonAuditDTO](
                    objects=frozenset([CarbonAuditDTO.from_entity(audit) for audit in audits]))
                assert actual_data == expected_data

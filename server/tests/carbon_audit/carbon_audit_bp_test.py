from datetime import datetime, timedelta

from flask.testing import FlaskClient

from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_dto import CarbonAuditDTO, CarbonAuditsGetResponse, CarbonAuditAddForm
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from tests.app_fixtures import AutoAppContextFixture
from tests.auth.auth_fixtures import AuthFixtures
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures
from tests.utils.dto_comparison_utils import patched_dto_for_comparison


class TestCarbonAuditEndpoint(DatabaseTest, AuthFixtures, UserFixtures, AutoAppContextFixture):
    class TestAdd:
        def test_add_audit(self, client: FlaskClient, users, access_headers_for):
            business = BusinessService.add("Mitchel's Bicycle Rental", facebook_url=None, creator_id=users.admin.id)
            form = CarbonAuditAddForm(
                business_id=business.id,
                score=50,
                report_date=datetime.utcnow().date(),
                report_url='https://reports.stc.org/10',
            )

            response = client.post('/carbon_audits/', json=form, headers=access_headers_for(users.carbon_auditor))

            assert response.status_code == 200
            with patched_dto_for_comparison(CarbonAuditDTO):
                actual_data = CarbonAuditDTO.model_validate(response.json)
                expected_data = CarbonAuditDTO(
                    id=0,
                    business_id=business.id,
                    creator_id=users.admin.id,
                    score=50,
                    report_date=datetime.utcnow().date(),
                    report_url='https://reports.stc.org/10',
                )
                assert actual_data == expected_data

    class TestGetAll:
        def test_get_audits(self, client: FlaskClient, users, access_headers_for):
            business = BusinessService.add("Mitchel's Bicycle Rental", facebook_url=None, creator_id=users.admin.id)
            audits = [CarbonAuditService.add(
                business_id=business.id,
                score=score,
                report_date=report_date,
                report_url='https://reports.stc.org/10',
                creator_id=users.admin.id,
            ) for score, report_date in [
                (84, datetime.utcnow().date() - timedelta(days=90)),
                (91, datetime.utcnow().date() - timedelta(days=60)),
                (85, datetime.utcnow().date() - timedelta(days=30)),
                (66, datetime.utcnow().date()),
            ]]

            response = client.get('/carbon_audits/', headers=access_headers_for(users.carbon_auditor))

            assert response.status_code == 200
            with patched_dto_for_comparison(CarbonAuditDTO):
                actual_data = CarbonAuditsGetResponse.model_validate(response.json)
                expected_data = CarbonAuditsGetResponse(
                    audits=frozenset([CarbonAuditDTO.from_entity(audit) for audit in audits]))
                assert actual_data == expected_data

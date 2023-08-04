from datetime import datetime, timedelta
from typing import Dict

import pytest
from flask.testing import FlaskClient

from app import app
from src.auth.auth_service import AuthService
from src.business.business_service import BusinessService
from src.carbon_audit.carbon_audit_dto import CarbonAuditDTO, CarbonAuditsGetResponse, CarbonAuditAddForm
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest
from tests.utils.dto_comparison_utils import patched_dto_for_comparison


class TestCarbonAuditEndpoint(DatabaseTest):

    @pytest.fixture(autouse=True)
    def setup_app_context(self) -> None:
        with app.app_context():
            yield

    @pytest.fixture
    def admin_id(self) -> int:
        return UserService.add_user('admin@stc.com', [UserRole.CARBON_AUDITOR]).id

    @pytest.fixture
    def access_headers(self, admin_id: int) -> Dict[str, str]:
        access_token = AuthService.create_access_token(admin_id)
        return {'Authorization': f'Bearer {access_token}'}

    class TestAdd:
        def test_add_audit(self,
                           client: FlaskClient,
                           admin_id: int,
                           access_headers: Dict[str, str]):
            business = BusinessService.add("Mitchel's Bicycle Rental", facebook_url=None, creator_id=admin_id)
            form = CarbonAuditAddForm(
                business_id=business.id,
                score=50,
                report_date=datetime.utcnow().date(),
                report_url='https://reports.stc.org/10',
            )

            response = client.post('/carbon_audits/', json=form, headers=access_headers)

            assert response.status_code == 200
            with patched_dto_for_comparison(CarbonAuditDTO):
                actual_data = CarbonAuditDTO.model_validate(response.json)
                expected_data = CarbonAuditDTO(
                    id=0,
                    business_id=business.id,
                    creator_id=admin_id,
                    score=50,
                    report_date=datetime.utcnow().date(),
                    report_url='https://reports.stc.org/10',
                )
                assert actual_data == expected_data

    class TestGetForUser:
        def test_get_audits(self,
                            client: FlaskClient,
                            admin_id: int,
                            access_headers: Dict[str, str]):
            business = BusinessService.add("Mitchel's Bicycle Rental", facebook_url=None, creator_id=admin_id)
            audits = [CarbonAuditService.add(
                business_id=business.id,
                score=score,
                report_date=report_date,
                report_url='https://reports.stc.org/10',
                creator_id=admin_id,
            ) for score, report_date in [
                (84, datetime.utcnow().date() - timedelta(days=90)),
                (91, datetime.utcnow().date() - timedelta(days=60)),
                (85, datetime.utcnow().date() - timedelta(days=30)),
                (66, datetime.utcnow().date()),
            ]]

            response = client.get('/carbon_audits/user', headers=access_headers)

            assert response.status_code == 200
            with patched_dto_for_comparison(CarbonAuditDTO):
                actual_data = CarbonAuditsGetResponse.model_validate(response.json)
                expected_data = CarbonAuditsGetResponse(
                    audits=frozenset([CarbonAuditDTO.from_entity(audit) for audit in audits]))
                assert actual_data == expected_data

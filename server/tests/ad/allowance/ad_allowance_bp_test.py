from typing import Dict

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask.testing import FlaskClient

from src.ad.allowance.ad_allowance_dto import AdAllowancesDTO, AdAllowanceDTO
from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.ad.allowance.ad_allowance_types import AdAllowance
from src.auth.auth_service import AuthService
from tests.app_fixtures import AutoAppContextFixture
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures


class TestAdAllowanceEndpoint(DatabaseTest, AutoAppContextFixture, UserFixtures):
    @pytest.fixture
    def access_headers(self, users) -> Dict[str, str]:
        access_token = AuthService.create_access_token(users.ad_manager.id)
        return {'Authorization': f'Bearer {access_token}'}

    def test_get_all(self,
                     client: FlaskClient,
                     access_headers: Dict[str, str],
                     monkeypatch: MonkeyPatch):
        monkeypatch.setattr(AdAllowanceService, 'get_for_all_businesses', lambda: {
            1: AdAllowance(full=10, used=5),
            2: AdAllowance(full=50, used=50),
            3: AdAllowance(full=1, used=0)
        })

        response = client.get('/ad-allowances/', headers=access_headers)

        assert response.status_code == 200
        actual_data = AdAllowancesDTO.model_validate(response.json)
        expected_data = AdAllowancesDTO(
            items=frozenset([
                AdAllowanceDTO(business_id=1, allowance=10, used_allowance=5),
                AdAllowanceDTO(business_id=2, allowance=50, used_allowance=50),
                AdAllowanceDTO(business_id=3, allowance=1, used_allowance=0)
            ]))
        assert actual_data == expected_data

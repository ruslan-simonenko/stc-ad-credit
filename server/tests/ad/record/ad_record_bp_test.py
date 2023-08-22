from datetime import datetime

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask.testing import FlaskClient

from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.ad.allowance.ad_allowance_types import AdAllowance
from src.ad.record.ad_record_dto import AdRecordAddFormDTO, AdRecordDTO, AdRecordsDTO, ErrorResponse
from src.ad.record.ad_record_service import AdRecordService
from src.persistence.schema.business import Business
from tests.app_fixtures import AutoAppContextFixture
from tests.auth.auth_fixtures import AuthFixtures
from tests.business.business_fixtures import BusinessFixtures
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures
from tests.utils.dto_comparison_utils import patched_dto_for_comparison

AD_POST_URL = 'https://facebook.com/groups/salisbury-noticeboard/posts/1643638762794779/'


class TestAdRecordEndpoint(DatabaseTest, BusinessFixtures, AuthFixtures, UserFixtures, AutoAppContextFixture):

    @pytest.fixture(autouse=True)
    def huge_ad_allowance(self, monkeypatch: MonkeyPatch):
        TestAdRecordEndpoint.mock_ad_allowance(monkeypatch, 1000)

    @pytest.fixture
    def no_ad_allowance(self, monkeypatch: MonkeyPatch):
        TestAdRecordEndpoint.mock_ad_allowance(monkeypatch, 0)

    class TestAdd:
        def test_add_ad_record(self, client: FlaskClient, users, access_headers_for, business: Business):
            form = AdRecordAddFormDTO(
                business_id=business.id,
                ad_post_url=AD_POST_URL,
            )

            response = client.post('/ad-records/', json=form, headers=access_headers_for(users.ad_manager))

            assert response.status_code == 200
            with patched_dto_for_comparison(AdRecordDTO):
                actual_data = AdRecordDTO.model_validate(response.json)
                expected_data = AdRecordDTO(
                    id=0,
                    business_id=business.id,
                    ad_post_url=AD_POST_URL,
                    creator_id=users.ad_manager.id,
                    created_at=datetime(year=1000, month=1, day=1),
                )
                assert actual_data == expected_data

        def test_insufficient_ad_allowance(self,
                                           client: FlaskClient,
                                           users,
                                           access_headers_for,
                                           business: Business,
                                           no_ad_allowance: None):
            form = AdRecordAddFormDTO(
                business_id=business.id,
                ad_post_url=AD_POST_URL,
            )

            response = client.post('/ad-records/', json=form, headers=access_headers_for(users.ad_manager))

            assert response.status_code == 403
            actual_response_data = ErrorResponse.model_validate(response.json)
            expected_response_data = ErrorResponse(message='Insufficient ad allowance')
            assert actual_response_data == expected_response_data

    class TestGetAll:
        def test_get_ad_records(self,
                                client: FlaskClient,
                                users,
                                access_headers_for,
                                business: Business):
            ad_records = [AdRecordService.add(
                business_id=business.id,
                ad_post_url=AD_POST_URL + ad_post_url_suffix,
                creator_id=users.ad_manager.id,
            ) for ad_post_url_suffix in ['a', 'b', 'c', 'd', 'e']]

            response = client.get('/ad-records/', headers=access_headers_for(users.ad_manager))

            assert response.status_code == 200
            with patched_dto_for_comparison(AdRecordDTO):
                actual_data = AdRecordsDTO.model_validate(response.json)
                expected_data = AdRecordsDTO(
                    records=frozenset([AdRecordDTO.from_entity(record) for record in ad_records]))
                assert actual_data == expected_data

    @staticmethod
    def mock_ad_allowance(monkeypatch: MonkeyPatch, value: int):
        monkeypatch.setattr(AdAllowanceService, 'get_for_business', lambda business_id: AdAllowance(full=value, used=0))

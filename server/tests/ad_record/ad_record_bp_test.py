from datetime import datetime
from typing import Dict

import pytest
from flask.testing import FlaskClient

from app import app
from src.ad_record.ad_record_dto import AdRecordAddFormDTO, AdRecordDTO, AdRecordsDTO
from src.ad_record.ad_record_service import AdRecordService
from src.auth.auth_service import AuthService
from src.business.business_service import BusinessService
from src.persistence.schema.user import User
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest
from tests.utils.dto_comparison_utils import patched_dto_for_comparison

AD_POST_URL = 'https://facebook.com/groups/salisbury-noticeboard/posts/1643638762794779/'


class TestAdRecordEndpoint(DatabaseTest):

    @pytest.fixture(autouse=True)
    def setup_app_context(self) -> None:
        with app.app_context():
            yield

    @pytest.fixture
    def user_ad_manager(self) -> User:
        return UserService.add_user('admin@stc.com', [UserRole.AD_MANAGER])

    @pytest.fixture
    def access_headers(self, user_ad_manager: User) -> Dict[str, str]:
        access_token = AuthService.create_access_token(user_ad_manager.id)
        return {'Authorization': f'Bearer {access_token}'}

    class TestAdd:
        def test_add_ad_record(self,
                               client: FlaskClient,
                               user_ad_manager: User,
                               access_headers: Dict[str, str]):
            business = BusinessService.add("Mitchel's Bicycle Rental", facebook_url=None, creator_id=user_ad_manager.id)
            form = AdRecordAddFormDTO(
                business_id=business.id,
                ad_post_url=AD_POST_URL,
            )

            response = client.post('/ad_records/', json=form, headers=access_headers)

            assert response.status_code == 200
            with patched_dto_for_comparison(AdRecordDTO):
                actual_data = AdRecordDTO.model_validate(response.json)
                expected_data = AdRecordDTO(
                    id=0,
                    business_id=business.id,
                    ad_post_url=AD_POST_URL,
                    creator_id=user_ad_manager.id,
                    created_at=datetime(year=1000, month=1, day=1),
                )
                assert actual_data == expected_data

    class TestGetAll:
        def test_get_ad_records(self,
                                client: FlaskClient,
                                user_ad_manager: User,
                                access_headers: Dict[str, str]):
            business = BusinessService.add("Mitchel's Bicycle Rental", facebook_url=None, creator_id=user_ad_manager.id)
            ad_records = [AdRecordService.add(
                business_id=business.id,
                ad_post_url=AD_POST_URL + ad_post_url_suffix,
                creator_id=user_ad_manager.id,
            ) for ad_post_url_suffix in ['a', 'b', 'c', 'd', 'e']]

            response = client.get('/ad_records/', headers=access_headers)

            assert response.status_code == 200
            with patched_dto_for_comparison(AdRecordDTO):
                actual_data = AdRecordsDTO.model_validate(response.json)
                expected_data = AdRecordsDTO(
                    records=frozenset([AdRecordDTO.from_entity(record) for record in ad_records]))
                assert actual_data == expected_data

from datetime import datetime, timedelta
from typing import List

import pytest
from _pytest.monkeypatch import MonkeyPatch

from app import app
from src.ad_record.ad_record_service import AdRecordService
from src.business.business_service import BusinessService
from src.persistence.schema.ad_record import AdRecord
from src.persistence.schema.business import Business
from src.persistence.schema.user import User
from src.user.user_service import UserService
from src.user.user_types import UserRole
from src.utils.clock import Clock
from tests.persistence.db_test import DatabaseTest


class TestAdRecordService(DatabaseTest):
    AD_POST_URL = 'https://facebook.com/groups/salisbury-noticeboard/posts/1643638762794779/'

    @pytest.fixture(autouse=True)
    def setup_app_context(self):
        with app.app_context():
            yield

    @pytest.fixture(autouse=True)
    def user_admin(self, setup_app_context) -> User:
        return UserService.add_user('admin@stc.com', [UserRole.ADMIN])

    @pytest.fixture(autouse=True)
    def user_ad_manager(self, setup_app_context) -> User:
        return UserService.add_user('ad-manager@stc.com', [UserRole.AD_MANAGER])

    @pytest.fixture
    def business(self, user_admin) -> Business:
        return BusinessService.add(name='Test Business', facebook_url=None, creator_id=user_admin.id)

    def test_add_ad_record(self, user_ad_manager: User, business: Business):
        ad_record = AdRecordService.add(
            business_id=business.id,
            ad_post_url=TestAdRecordService.AD_POST_URL,
            creator_id=user_ad_manager.id,
        )
        assert ad_record.business_id == business.id
        assert ad_record.ad_post_url == TestAdRecordService.AD_POST_URL
        assert ad_record.created_by == user_ad_manager.id
        assert datetime.utcnow() - ad_record.created_at < timedelta(minutes=1)

    def test_add_multiple_records_for_a_business(self, user_ad_manager: User, business: Business):
        for ad_post_url_suffix in ['a', 'b', 'c']:
            ad_record = AdRecordService.add(
                business_id=business.id,
                ad_post_url=TestAdRecordService.AD_POST_URL + ad_post_url_suffix,
                creator_id=user_ad_manager.id,
            )
            assert ad_record.business_id == business.id
            assert ad_record.ad_post_url == TestAdRecordService.AD_POST_URL + ad_post_url_suffix
            assert ad_record.created_by == user_ad_manager.id
            assert datetime.utcnow() - ad_record.created_at < timedelta(minutes=1)

    class TestGetAll:
        @pytest.fixture
        def ad_records(self, user_ad_manager: User, business: Business) -> List[AdRecord]:
            return [AdRecordService.add(
                business_id=business.id,
                ad_post_url=TestAdRecordService.AD_POST_URL + ad_post_url_suffix,
                creator_id=user_ad_manager.id,
            ) for ad_post_url_suffix in ['a', 'b', 'c', 'd', 'e']]

        def test_get_all(self, ad_records: List[AdRecord]):
            actual_ad_records = AdRecordService.get_all()
            assert actual_ad_records == list(reversed(ad_records))

    class TestGetCountForBusinessSinceDate:

        @pytest.fixture(autouse=True)
        def ad_records(self, user_ad_manager: User, business: Business, monkeypatch: MonkeyPatch):
            current_time = datetime.utcnow()
            for days_ago in [120, 100, 90, 70, 50, 44, 37, 32, 11, 3]:
                monkeypatch.setattr(Clock, 'now', lambda: current_time - timedelta(days=days_ago))
                AdRecordService.add(
                    business_id=business.id,
                    ad_post_url=TestAdRecordService.AD_POST_URL,
                    creator_id=user_ad_manager.id,
                )
            monkeypatch.undo()

        @pytest.mark.parametrize('since_days_ago, include_days_report, expected_count', [
            (0, True, 0),
            (1, True, 0),
            (2, True, 0),
            (3, False, 0),
            (3, True, 1),
            (10, True, 1),
            (11, True, 2),
            (38, False, 4),
            (70, True, 7),
            (200, False, 10),
        ])
        def test_returns_valid_count(self, since_days_ago: int, include_days_report: bool, expected_count: int,
                                     business: Business):
            since_time = datetime.utcnow() \
                         - timedelta(days=since_days_ago) \
                         - (timedelta(minutes=1) if include_days_report else timedelta(seconds=0))
            actual_count = AdRecordService.get_count_for_business_since_date(business_id=business.id, since=since_time)
            assert actual_count == expected_count

        def test_businesses_are_isolated(self, business: Business, user_admin: User, user_ad_manager: User):
            other_business = BusinessService.add(name='Awesome carpet cleaners', facebook_url=None,
                                                 creator_id=user_admin.id)
            for i in range(3):
                AdRecordService.add(
                    business_id=business.id,
                    ad_post_url=TestAdRecordService.AD_POST_URL,
                    creator_id=user_ad_manager.id,
                )
            for i in range(2):
                AdRecordService.add(
                    business_id=other_business.id,
                    ad_post_url=TestAdRecordService.AD_POST_URL,
                    creator_id=user_ad_manager.id,
                )

            since_time = datetime.utcnow() - timedelta(minutes=1)
            actual_count_first = AdRecordService.get_count_for_business_since_date(business_id=business.id,
                                                                                   since=since_time)
            actual_count_second = AdRecordService.get_count_for_business_since_date(business_id=other_business.id,
                                                                                    since=since_time)
            assert actual_count_first == 3
            assert actual_count_second == 2

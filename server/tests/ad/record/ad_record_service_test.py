from datetime import datetime, timedelta
from typing import List

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.ad.record.ad_record_service import AdRecordService
from src.persistence.schema.ad_record import AdRecord
from src.utils.clock import Clock
from tests.app_fixtures import AutoAppContextFixture
from tests.business.business_fixtures import BusinessFixtures
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures

AD_POST_URL = 'https://facebook.com/groups/salisbury-noticeboard/posts/1643638762794779/'


class TestAdRecordService(DatabaseTest, AutoAppContextFixture, BusinessFixtures, UserFixtures):
    AD_POST_URL = 'https://facebook.com/groups/salisbury-noticeboard/posts/1643638762794779/'

    def test_add_ad_record(self, users, business):
        ad_record = AdRecordService.add(
            business_id=business.id,
            ad_post_url=TestAdRecordService.AD_POST_URL,
            creator_id=users.ad_manager.id,
        )
        assert ad_record.business_id == business.id
        assert ad_record.ad_post_url == TestAdRecordService.AD_POST_URL
        assert ad_record.created_by == users.ad_manager.id
        assert datetime.utcnow() - ad_record.created_at < timedelta(minutes=1)

    def test_add_multiple_records_for_a_business(self, users, business):
        for ad_post_url_suffix in ['a', 'b', 'c']:
            ad_record = AdRecordService.add(
                business_id=business.id,
                ad_post_url=TestAdRecordService.AD_POST_URL + ad_post_url_suffix,
                creator_id=users.ad_manager.id,
            )
            assert ad_record.business_id == business.id
            assert ad_record.ad_post_url == TestAdRecordService.AD_POST_URL + ad_post_url_suffix
            assert ad_record.created_by == users.ad_manager.id
            assert datetime.utcnow() - ad_record.created_at < timedelta(minutes=1)

    class TestGetAll:
        @pytest.fixture
        def ad_records(self, users, business) -> List[AdRecord]:
            return [AdRecordService.add(
                business_id=business.id,
                ad_post_url=TestAdRecordService.AD_POST_URL + ad_post_url_suffix,
                creator_id=users.ad_manager.id,
            ) for ad_post_url_suffix in ['a', 'b', 'c', 'd', 'e']]

        def test_get_all(self, ad_records: List[AdRecord]):
            actual_ad_records = AdRecordService.get_all()
            assert actual_ad_records == list(reversed(ad_records))

    class TestGetCountForBusinessSinceDate:

        @pytest.fixture
        def ad_records(self, users, business, monkeypatch: MonkeyPatch):
            current_time = datetime.utcnow()
            for days_ago in [120, 100, 90, 70, 50, 44, 37, 32, 11, 3]:
                monkeypatch.setattr(Clock, 'now', lambda: current_time - timedelta(days=days_ago))
                AdRecordService.add(
                    business_id=business.id,
                    ad_post_url=TestAdRecordService.AD_POST_URL,
                    creator_id=users.ad_manager.id,
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
                                     business, ad_records):
            since_time = datetime.utcnow() \
                         - timedelta(days=since_days_ago) \
                         - (timedelta(minutes=1) if include_days_report else timedelta(seconds=0))
            actual_count = AdRecordService.get_count_for_business_since_date(business_id=business.id,
                                                                             since=since_time)
            assert actual_count == expected_count

        def test_businesses_are_isolated(self, businesses, users):
            for i in range(3):
                AdRecordService.add(
                    business_id=businesses.apple.id,
                    ad_post_url=TestAdRecordService.AD_POST_URL,
                    creator_id=users.ad_manager.id,
                )
            for i in range(2):
                AdRecordService.add(
                    business_id=businesses.banana.id,
                    ad_post_url=TestAdRecordService.AD_POST_URL,
                    creator_id=users.ad_manager.id,
                )

            since_time = datetime.utcnow() - timedelta(minutes=1)
            actual_count_apple = AdRecordService.get_count_for_business_since_date(business_id=businesses.apple.id,
                                                                                   since=since_time)
            actual_count_banana = AdRecordService.get_count_for_business_since_date(business_id=businesses.banana.id,
                                                                                    since=since_time)
            assert actual_count_apple == 3
            assert actual_count_banana == 2

    class TestGetCountForAllBusinessesSinceDate:

        def test_get_no_records(self, businesses):
            result = AdRecordService.get_count_for_all_businesses_since_date(since=datetime.utcnow())
            assert result == {businesses.apple.id: 0,
                              businesses.banana.id: 0,
                              businesses.pear.id: 0}

        def test_get_count(self, businesses, users, monkeypatch: MonkeyPatch):
            now = datetime.utcnow()
            for business_id, records_days_ago in {businesses.apple.id: [30, 15, 10],
                                                  businesses.banana.id: [50, 7, 5, 1],
                                                  businesses.pear.id: [100, 80, 12]}.items():
                for days_ago in records_days_ago:
                    monkeypatch.setattr(Clock, 'now', lambda: now - timedelta(days=days_ago))
                    AdRecordService.add(business_id, ad_post_url=AD_POST_URL, creator_id=users.ad_manager.id)

            result = AdRecordService.get_count_for_all_businesses_since_date(since=now - timedelta(days=20))
            assert result == {businesses.apple.id: 2,
                              businesses.banana.id: 3,
                              businesses.pear.id: 1}

        def test_get_count_since_dates(self, businesses, users, monkeypatch: MonkeyPatch):
            now = datetime.utcnow()
            for business_id, records_days_ago in {businesses.apple.id: [45, 30, 15, 10],
                                                  businesses.banana.id: [50, 7, 5, 1],
                                                  businesses.pear.id: [100, 80, 12]}.items():
                for days_ago in records_days_ago:
                    monkeypatch.setattr(Clock, 'now', lambda: now - timedelta(days=days_ago))
                    AdRecordService.add(business_id, ad_post_url=AD_POST_URL, creator_id=users.ad_manager.id)

            result = AdRecordService.get_count_for_all_businesses_since_dates({
                businesses.apple.id: now - timedelta(days=15),
                businesses.banana.id: now - timedelta(days=4),
                businesses.pear.id: now - timedelta(days=130),
            })
            assert result == {businesses.apple.id: 2,
                              businesses.banana.id: 1,
                              businesses.pear.id: 3}

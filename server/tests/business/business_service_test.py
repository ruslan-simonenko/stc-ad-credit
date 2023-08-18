from datetime import datetime, timedelta

import pytest

from src.business.business_service import BusinessService
from tests.app_fixtures import AutoAppContextFixture
from tests.business.business_test_utils import BusinessTestUtils
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures


class TestBusinessService(DatabaseTest, AutoAppContextFixture, UserFixtures):

    @pytest.mark.parametrize('name, facebook_url', [
        ('test business', None),
        ('test business', 'https://www.facebook.com/groups/seethroughnews/'),
    ])
    def test_add_business(self, users, name, facebook_url):
        business = BusinessService.add(name=name, facebook_url=facebook_url, creator_id=users.business_manager.id)
        assert business.name == name
        assert business.facebook_url == facebook_url
        assert business.created_by == users.business_manager.id
        assert datetime.utcnow() - business.created_at < timedelta(minutes=1)

    def test_add_business_duplicate_name(self, users):
        BusinessTestUtils.add_business(users.business_manager, name='test business')
        with pytest.raises(ValueError, match='Business name is already in use'):
            BusinessTestUtils.add_business(users.business_manager, name='test business')

    def test_get_all_businesses(self, users):
        expected_businesses = {BusinessTestUtils.add_business(users.business_manager) for _ in range(3)}
        actual_businesses = BusinessService.get_all()
        assert set(actual_businesses) == expected_businesses

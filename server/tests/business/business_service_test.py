from datetime import datetime, timedelta

import pytest

from src.business.business_service import BusinessService
from tests.app_fixtures import AutoAppContextFixture
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures


class TestBusinessService(DatabaseTest, AutoAppContextFixture, UserFixtures):

    @pytest.mark.parametrize('name, facebook_url', [
        ('test business', None),
        ('test business', 'https://www.facebook.com/groups/seethroughnews/'),
    ])
    def test_add_business(self, users, name, facebook_url):
        business = BusinessService.add(name=name, facebook_url=facebook_url, creator_id=users.admin.id)
        assert business.name == name
        assert business.facebook_url == facebook_url
        assert business.created_by == users.admin.id
        assert datetime.utcnow() - business.created_at < timedelta(minutes=1)

    def test_add_business_duplicate_name(self, users):
        BusinessService.add(name='test business', facebook_url=None, creator_id=users.admin.id)
        with pytest.raises(ValueError, match='Business name is already in use'):
            BusinessService.add(name='test business', facebook_url=None, creator_id=users.admin.id)

    def test_get_all_businesses(self, users):
        biz_a = BusinessService.add('test biz a', facebook_url=None, creator_id=users.admin.id)
        biz_b = BusinessService.add('test biz b', facebook_url='https://facebook.com/apage', creator_id=users.admin.id)
        biz_c = BusinessService.add('test biz c', facebook_url=None, creator_id=users.admin.id)
        actual_businesses = BusinessService.get_all()
        assert set(actual_businesses) == {biz_a, biz_b, biz_c}

from datetime import datetime, timedelta

import pytest

from app import app
from src.business.business_service import BusinessService
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest


class TestBusinessService(DatabaseTest):

    @pytest.fixture(autouse=True)
    def setup_app_context(self):
        with app.app_context():
            yield

    @pytest.fixture(autouse=True)
    def current_user(self, setup_app_context):
        return UserService.add_user('test@gmail.com', [UserRole.ADMIN])

    @pytest.mark.parametrize('name, facebook_url', [
        ('test business', None),
        ('test business', 'https://www.facebook.com/groups/seethroughnews/'),
    ])
    def test_add_business(self, current_user, name, facebook_url):
        business = BusinessService.add(name=name, facebook_url=facebook_url, creator=current_user)
        assert business.name == name
        assert business.facebook_url == facebook_url
        assert business.created_by == current_user.id
        assert datetime.utcnow() - business.created_at < timedelta(minutes=1)

    def test_add_business_duplicate_name(self, current_user):
        BusinessService.add(name='test business', facebook_url=None, creator=current_user)
        with pytest.raises(ValueError, match='Business name is already in use'):
            BusinessService.add(name='test business', facebook_url=None, creator=current_user)

    def test_get_all_businesses(self, current_user):
        biz_a = BusinessService.add('test biz a', facebook_url=None, creator=current_user)
        biz_b = BusinessService.add('test biz b', facebook_url='https://facebook.com/somepage', creator=current_user)
        biz_c = BusinessService.add('test biz c', facebook_url=None, creator=current_user)
        actual_businesses = BusinessService.get_all()
        assert set(actual_businesses) == {biz_a, biz_b, biz_c}


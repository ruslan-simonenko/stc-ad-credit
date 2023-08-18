from datetime import datetime, timedelta

import pytest

from src.business.business_service import BusinessService
from src.business.business_types import BusinessRegistrationType
from tests.app_fixtures import AutoAppContextFixture
from tests.business.business_test_utils import BusinessTestUtils
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures


class TestBusinessService(DatabaseTest, AutoAppContextFixture, UserFixtures):

    @pytest.mark.parametrize('name, reg_type, reg_number, email, facebook_url', [
        ('only basic info', BusinessRegistrationType.NI, 'QQ123456C', None, None),
        ('email only', BusinessRegistrationType.CRN, 'IP123456', 'wonderful-pastries@gmail.com', None),
        ('facebook url only', BusinessRegistrationType.VAT, 'GB123456789', None, 'https://facebook.com/fb_url'),
        ('all', BusinessRegistrationType.VAT, 'GB123456789', 'stc@stc.org', 'https://facebook.com/fb_url'),
    ])
    def test_add_business(self, users, name, reg_type, reg_number, email, facebook_url):
        business = BusinessService.add(name=name,
                                       registration_type=reg_type,
                                       registration_number=reg_number,
                                       email=email,
                                       facebook_url=facebook_url,
                                       creator_id=users.business_manager.id)
        assert business.name == name
        assert business.registration_type == reg_type
        assert business.registration_number == reg_number
        assert business.email == email
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

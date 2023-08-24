from datetime import datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from src.business.business_service import BusinessService
from src.business.business_types import BusinessRegistrationType
from src.persistence.schema.business import Business
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
        name = 'test business'
        BusinessTestUtils.add_business(users.business_manager, name=name)
        with pytest.raises(IntegrityError):
            BusinessTestUtils.add_business(users.business_manager, name=name)

    def test_add_business_duplicate_registration(self, users):
        reg_type = BusinessRegistrationType.NI
        reg_number = 'GB123456789'
        BusinessTestUtils.add_business(users.business_manager, registration_type=reg_type,
                                       registration_number=reg_number)
        with pytest.raises(IntegrityError):
            BusinessTestUtils.add_business(users.business_manager, registration_type=reg_type,
                                           registration_number=reg_number)

    def test_get_all_businesses(self, users):
        expected_businesses = {BusinessTestUtils.add_business(users.business_manager) for _ in range(3)}
        actual_businesses = BusinessService.get_all()
        assert set(actual_businesses) == expected_businesses

    class TestUpdate:
        NEW_NAME = 'updated_business'
        NEW_REG_TYPE = BusinessRegistrationType.NI
        NEW_REG_NUMBER = 'GB123456789'
        NEW_EMAIL = 'new-email@gmail.com'
        NEW_FACEBOOK_URL = 'https://facebook.com/updated-business'

        def test_update_business(self, users):
            def assert_business_updated(business: Business):
                assert business.name == self.NEW_NAME
                assert business.registration_type == self.NEW_REG_TYPE
                assert business.registration_number == self.NEW_REG_NUMBER
                assert business.email == self.NEW_EMAIL
                assert business.facebook_url == self.NEW_FACEBOOK_URL

            original_business = BusinessTestUtils.add_business(users.business_manager)

            updated_business = BusinessService.update(
                business_id=original_business.id, name=self.NEW_NAME, registration_type=self.NEW_REG_TYPE,
                registration_number=self.NEW_REG_NUMBER, email=self.NEW_EMAIL, facebook_url=self.NEW_FACEBOOK_URL)
            assert_business_updated(updated_business)
            post_update_business = BusinessService.get_by_id_or_throw(business_id=original_business.id)
            assert_business_updated(post_update_business)

        def test_update_business_partially(self, users):
            original_business = BusinessTestUtils.add_business(users.business_manager)

            def assert_business_updated(business: Business):
                assert business.name == original_business.name
                assert business.registration_type == self.NEW_REG_TYPE
                assert business.registration_number == self.NEW_REG_NUMBER
                assert business.email == original_business.email
                assert business.facebook_url == self.NEW_FACEBOOK_URL

            updated_business = BusinessService.update(
                business_id=original_business.id, registration_type=self.NEW_REG_TYPE,
                registration_number=self.NEW_REG_NUMBER, facebook_url=self.NEW_FACEBOOK_URL)
            assert_business_updated(updated_business)
            post_update_business = BusinessService.get_by_id_or_throw(business_id=original_business.id)
            assert_business_updated(post_update_business)

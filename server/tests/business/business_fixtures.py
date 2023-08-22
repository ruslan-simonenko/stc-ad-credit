from typing import NamedTuple

import pytest

from src.persistence.schema.business import Business
from tests.business.business_test_utils import BusinessTestUtils
from tests.user.user_fixtures import UserFixtures


class BusinessFixtures(UserFixtures):
    class Businesses(NamedTuple):
        apple: Business
        banana: Business
        pear: Business

    @pytest.fixture
    def business(self, users) -> Business:
        return BusinessTestUtils.add_business(users.business_manager, name='Apple')

    @pytest.fixture
    def businesses(self, users) -> Businesses:
        apple = BusinessTestUtils.add_business(users.business_manager, name='Apple')
        banana = BusinessTestUtils.add_business(users.business_manager, name='Banana')
        pear = BusinessTestUtils.add_business(users.business_manager, name='Pear')
        return self.Businesses(apple, banana, pear)

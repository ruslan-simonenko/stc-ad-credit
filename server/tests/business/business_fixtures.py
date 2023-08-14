from typing import NamedTuple

import pytest

from src.business.business_service import BusinessService
from src.persistence.schema.business import Business
from tests.user.user_fixtures import UserFixtures


class BusinessFixtures(UserFixtures):
    class Businesses(NamedTuple):
        apple: Business
        banana: Business
        pear: Business

    @pytest.fixture
    def business(self, users) -> Business:
        return BusinessService.add(name='Apple', facebook_url=None, creator_id=users.admin.id)

    @pytest.fixture
    def businesses(self, users) -> Businesses:
        apple = BusinessService.add(name='Apple', facebook_url=None, creator_id=users.admin.id)
        banana = BusinessService.add(name='Banana', facebook_url=None, creator_id=users.admin.id)
        pear = BusinessService.add(name='Pear', facebook_url=None, creator_id=users.admin.id)
        return self.Businesses(apple, banana, pear)

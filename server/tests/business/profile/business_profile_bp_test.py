from flask.testing import FlaskClient

from src.persistence.schema.business import Business
from tests.app_fixtures import AutoAppContextFixture
from tests.business.business_fixtures import BusinessFixtures
from tests.persistence.db_test import DatabaseTest


class TestBusinessProfileEndpoint(DatabaseTest, AutoAppContextFixture, BusinessFixtures):
    def test_get_profile(self, client: FlaskClient, business: Business):
        response = client.get(f'/businesses/{business.id}/profile')

        assert response.status_code == 200
        assert response.text.find(business.name) != -1

from flask.testing import FlaskClient

from app import app
from src.business.business_dto import BusinessAddForm, BusinessDTO
from src.business.business_types import BusinessRegistrationType
from src.utils.dto import ResponseWithObject, ResponseWithObjects
from tests.app_fixtures import AutoAppContextFixture
from tests.auth.auth_fixtures import AuthFixtures
from tests.business.business_test_utils import BusinessTestUtils
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures
from tests.utils.dto_comparison_utils import patched_dto_for_comparison


class TestBusinessEndpoint(DatabaseTest, AuthFixtures, UserFixtures, AutoAppContextFixture):

    def test_add(self, client: FlaskClient, users, access_headers_for, monkeypatch):
        form = BusinessAddForm(name='Fabulous Pastries',
                               registration_type=BusinessRegistrationType.VAT,
                               registration_number='GB123456789',
                               email='pastries@gmail.com',
                               facebook_url='https://facebook.com/best-pastries')
        response = client.post('/businesses', json=form, headers=access_headers_for(users.business_manager))

        assert response.status_code == 200
        with patched_dto_for_comparison(BusinessDTO):
            created_business = ResponseWithObject[BusinessDTO].model_validate(response.json).object
            expected_business = BusinessDTO(
                id=0,
                name=form.name,
                registration_type=form.registration_type,
                registration_number=form.registration_number,
                email=form.email,
                facebook_url=form.facebook_url
            )
            assert created_business == expected_business

    def test_get_all(self, client: FlaskClient, users, access_headers_for):
        with app.app_context():
            businesses_dtos = [
                BusinessDTO.from_entity(BusinessTestUtils.add_business(creator=users.business_manager))
                for _ in range(3)
            ]

        response = client.get('/businesses', headers=access_headers_for(users.business_manager))

        assert response.status_code == 200
        with patched_dto_for_comparison(BusinessDTO):
            actual_data = ResponseWithObjects[BusinessDTO].model_validate(response.json)
            expected_data = ResponseWithObjects[BusinessDTO](objects=frozenset(businesses_dtos))
            assert actual_data == expected_data
            assert len({business.id for business in actual_data.objects}) == len(businesses_dtos)

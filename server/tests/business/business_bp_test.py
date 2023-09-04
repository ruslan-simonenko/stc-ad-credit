from typing import List

import pytest
from flask.testing import FlaskClient
from pydantic import ValidationError

from src.business.business_dto import BusinessAddForm, BusinessDTO, BusinessDTOPublic, BusinessUpdateForm
from src.business.business_service import BusinessService
from src.business.business_types import BusinessRegistrationType
from src.persistence.schema.business import Business
from src.utils.dto import ResponseWithObject, ResponseWithObjects
from tests.app_fixtures import AutoAppContextFixture
from tests.auth.auth_fixtures import AuthFixtures
from tests.business.business_test_utils import BusinessTestUtils
from tests.persistence.db_test import DatabaseTest
from tests.user.user_fixtures import UserFixtures
from tests.utils.dto_comparison_utils import patched_dto_for_comparison


class TestBusinessEndpoint(DatabaseTest, AuthFixtures, UserFixtures, AutoAppContextFixture):
    class TestAdd:

        def test_add_ad_manager__known(self, client: FlaskClient, users, access_headers_for):
            form = BusinessAddForm(name='Fabulous Pastries',
                                   registration_type=BusinessRegistrationType.KNOWN,
                                   registration_number='random-meaninglessness',
                                   email=None,
                                   facebook_url='https://facebook.com/best-pastries')
            response = client.post('/businesses', json=form, headers=access_headers_for(users.ad_manager))

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

        def test_add_ad_manager__registered(self, client: FlaskClient, users, access_headers_for):
            form = BusinessAddForm(name='Fabulous Pastries',
                                   registration_type=BusinessRegistrationType.VAT,
                                   registration_number='GB123456789',
                                   email=None,
                                   facebook_url='https://facebook.com/best-pastries')
            response = client.post('/businesses', json=form, headers=access_headers_for(users.ad_manager))

            assert response.status_code == 403

        def test_add_business_manager(self, client: FlaskClient, users, access_headers_for):
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

    class TestUpdate:

        def test_update_business_manager(self, client: FlaskClient, users, access_headers_for):
            business = BusinessTestUtils.add_business(users.business_manager)

            form = BusinessUpdateForm(
                name='Fabulous Pastries',
                registration_type=BusinessRegistrationType.VAT,
                registration_number='GB123456789',
                email='pastries@gmail.com',
                facebook_url='https://facebook.com/best-pastries')
            response = client.put(f'/businesses/{business.id}', json=form,
                                  headers=access_headers_for(users.business_manager))

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

        def test_update_ad_manager(self, client: FlaskClient, users, access_headers_for):
            business = BusinessTestUtils.add_business(users.business_manager)

            form = BusinessUpdateForm(
                name='Fabulous Pastries',
                registration_type=BusinessRegistrationType.KNOWN,
                registration_number='random-string',
                email='pastries@gmail.com',
                facebook_url='https://facebook.com/best-pastries')
            response = client.put(f'/businesses/{business.id}', json=form, headers=access_headers_for(users.ad_manager))

            assert response.status_code == 200
            # No sensitive data is returned
            with pytest.raises(ValidationError, match='3 validation errors'):
                ResponseWithObject[BusinessDTO].model_validate(response.json)
            # Updated model is returned
            with patched_dto_for_comparison(BusinessDTOPublic):
                created_business = ResponseWithObject[BusinessDTOPublic].model_validate(response.json).object
                expected_business = BusinessDTOPublic(
                    id=0,
                    name=form.name,
                    facebook_url=form.facebook_url
                )
                assert created_business == expected_business
            # Sensitive fields are not updated
            updated_business = BusinessService.get_by_id_or_throw(business.id)
            assert updated_business.registration_type == business.registration_type
            assert updated_business.registration_number == business.registration_number
            assert updated_business.email == business.email

    class TestGetAll:
        @pytest.fixture
        def businesses(self, users) -> List[Business]:
            return [BusinessTestUtils.add_business(creator=users.business_manager) for _ in range(3)]

        def test_business_manager(self, client: FlaskClient, users, access_headers_for, businesses):
            response = client.get('/businesses', headers=access_headers_for(users.business_manager))

            assert response.status_code == 200
            with patched_dto_for_comparison(BusinessDTO):
                actual_data = ResponseWithObjects[BusinessDTO].model_validate(response.json)
                expected_data = ResponseWithObjects[BusinessDTO](
                    objects=frozenset([BusinessDTO.from_entity(e) for e in businesses]))
                assert actual_data == expected_data
                assert len({business.id for business in actual_data.objects}) == len(businesses)

        @pytest.mark.parametrize('user_key', ['ad_manager', 'admin', 'carbon_auditor'])
        def test_other_roles(self, client: FlaskClient, users, access_headers_for, businesses, user_key):
            response = client.get('/businesses', headers=access_headers_for(getattr(users, user_key)))

            assert response.status_code == 200
            with patched_dto_for_comparison(BusinessDTOPublic):
                actual_data = ResponseWithObjects[BusinessDTOPublic].model_validate(response.json)
                expected_data = ResponseWithObjects[BusinessDTOPublic](
                    objects=frozenset([BusinessDTOPublic.from_entity(e) for e in businesses]))
                assert actual_data == expected_data
                assert len({business.id for business in actual_data.objects}) == len(businesses)

        @pytest.mark.parametrize('user_key', ['ad_manager', 'admin', 'carbon_auditor'])
        def test_sensitive_fields_not_sent_to_other_roles(self, client: FlaskClient, users, access_headers_for,
                                                          businesses, user_key):
            response = client.get('/businesses', headers=access_headers_for(getattr(users, user_key)))

            assert response.status_code == 200
            with pytest.raises(ValidationError):
                ResponseWithObjects[BusinessDTO].model_validate(response.json)

from typing import List

import pytest
from flask.testing import FlaskClient
from pydantic import ValidationError

from src.business.business_dto import BusinessAddForm, BusinessDTO, BusinessDTOPublic
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

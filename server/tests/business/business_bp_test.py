from typing import Dict

import pytest
from flask.testing import FlaskClient

from app import app
from src.auth.auth_service import AuthService
from src.business.business_dto import BusinessAddForm, BusinessDTO, BusinessOperationSuccessResponse, \
    BusinessesGetAllResponse
from src.business.business_service import BusinessService
from src.user.user_service import UserService
from src.user.user_types import UserRole
from tests.persistence.db_test import DatabaseTest
from tests.utils.dto_comparison_utils import patched_dto_for_comparison


class TestBusinessEndpoint(DatabaseTest):
    admin_id: int

    @pytest.fixture
    def access_headers(self) -> Dict[str, str]:
        with app.app_context():
            admin = UserService.add_user('admin@stc.com', [UserRole.ADMIN])
            self.admin_id = admin.id
            access_token = AuthService.create_access_token(admin.id)
        return {'Authorization': f'Bearer {access_token}'}

    def test_add(self, client: FlaskClient, access_headers: Dict[str, str]):
        form = BusinessAddForm(name='Fabulous Pastries', facebook_url='https://facebook.com/best-pastries')
        response = client.post('/businesses', json=form, headers=access_headers)

        assert response.status_code == 200
        with patched_dto_for_comparison(BusinessDTO):
            created_business = BusinessOperationSuccessResponse.model_validate(response.json)
            expected_business = BusinessOperationSuccessResponse(business=BusinessDTO(
                id=0,
                name=form.name,
                facebook_url=form.facebook_url
            ))
            assert created_business == expected_business

    def test_get_all(self, client: FlaskClient, access_headers: Dict[str, str]):
        with app.app_context():
            business_dutch = BusinessService.add(name='Fabulous Dutch Pastries',
                                                 facebook_url='https://facebook.com/best-dutch-pastries',
                                                 creator_id=self.admin_id)
            business_welsh = BusinessService.add(name='Awesome Welsh Cuisine',
                                                 facebook_url='https://facebook.com/the-welsh-cuisine',
                                                 creator_id=self.admin_id)
            businesses_dtos = [
                BusinessDTO.from_entity(business_dutch),
                BusinessDTO.from_entity(business_welsh)
            ]

        response = client.get('/businesses', headers=access_headers)

        assert response.status_code == 200
        with patched_dto_for_comparison(BusinessDTO):
            actual_data = BusinessesGetAllResponse.model_validate(response.json)
            expected_data = BusinessesGetAllResponse(businesses=frozenset(businesses_dtos))
            assert actual_data == expected_data
            assert len({business.id for business in actual_data.businesses}) == len(businesses_dtos)

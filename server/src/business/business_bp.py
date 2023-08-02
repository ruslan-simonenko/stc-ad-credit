from flask import Blueprint, jsonify, request

from src.auth.auth_bp import auth_role
from src.auth.auth_service import AuthService
from src.business.business_dto import BusinessDTO, BusinessesGetAllResponse, BusinessAddForm, \
    BusinessOperationSuccessResponse
from src.business.business_service import BusinessService
from src.user.user_types import UserRole

business_bp = Blueprint('business', __name__, url_prefix='/businesses')


@business_bp.route('/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.CARBON_AUDITOR)
def get_all():
    businesses = [BusinessDTO.from_entity(business) for business in BusinessService.get_all()]
    return jsonify(BusinessesGetAllResponse(businesses=businesses))


@business_bp.route('/', methods=['post'])
@auth_role(UserRole.ADMIN, UserRole.CARBON_AUDITOR)
def add():
    form = BusinessAddForm.model_validate(request.get_json())
    trimmed_name = str.strip(form.name)
    trimmed_facebook_url = str.strip(form.facebook_url)
    business = BusinessService.add(
        name=trimmed_name,
        facebook_url=trimmed_facebook_url if trimmed_facebook_url else None,
        creator_id=AuthService.get_current_user_id_or_throw())
    return jsonify(BusinessOperationSuccessResponse(business=BusinessDTO.from_entity(business)))

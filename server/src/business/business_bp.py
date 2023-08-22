from flask import Blueprint, jsonify, request

from src.auth.auth_bp import auth_role
from src.auth.auth_service import AuthService
from src.business.business_dto import BusinessDTO, BusinessAddForm
from src.business.business_service import BusinessService
from src.business.profile.business_profile_bp import business_profile_bp
from src.user.user_types import UserRole
from src.utils.dto import ResponseWithObjects, ResponseWithObject

business_bp = Blueprint('business', __name__, url_prefix='/businesses')
business_bp.register_blueprint(business_profile_bp)


@business_bp.route('/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.AD_MANAGER, UserRole.CARBON_AUDITOR, UserRole.BUSINESS_MANAGER)
def get_all():
    businesses = [BusinessDTO.from_entity(business) for business in BusinessService.get_all()]
    return jsonify(ResponseWithObjects[BusinessDTO](objects=businesses))


@business_bp.route('/', methods=['post'])
@auth_role(UserRole.ADMIN, UserRole.BUSINESS_MANAGER)
def add():
    form = BusinessAddForm.model_validate(request.get_json())
    business = BusinessService.add(
        name=form.name,
        registration_type=form.registration_type,
        registration_number=form.registration_number,
        email=form.email,
        facebook_url=form.facebook_url,
        creator_id=AuthService.get_current_user_id_or_throw())
    return jsonify(ResponseWithObject[BusinessDTO](object=BusinessDTO.from_entity(business)))

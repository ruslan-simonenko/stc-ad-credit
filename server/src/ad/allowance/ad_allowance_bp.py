from flask import Blueprint, jsonify

from src.ad.allowance.ad_allowance_dto import AdAllowanceDTO
from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.auth.auth_bp import auth_role
from src.user.user_types import UserRole
from src.utils.dto import ResponseWithObjects

ad_allowance_bp = Blueprint('ad_allowance', __name__, url_prefix='/ad-allowances')


@ad_allowance_bp.route('/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.CARBON_AUDITOR, UserRole.AD_MANAGER)
def get_all():
    allowances = AdAllowanceService.get_for_all_businesses()
    dtos = [AdAllowanceDTO(business_id=business_id, window_start=allowance.window_start, allowance=allowance.full,
                           used_allowance=allowance.used)
            for business_id, allowance in allowances.items()]
    return jsonify(ResponseWithObjects[AdAllowanceDTO](objects=dtos))

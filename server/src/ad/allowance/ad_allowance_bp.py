from flask import Blueprint, jsonify

from src.ad.allowance.ad_allowance_dto import AdAllowanceDTO, AdAllowancesDTO
from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.auth.auth_bp import auth_role
from src.user.user_types import UserRole

ad_allowance_bp = Blueprint('ad_allowance', __name__, url_prefix='/ad-allowances')


@ad_allowance_bp.route('/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.AD_MANAGER)
def get_all():
    allowances = AdAllowanceService.get_for_all_businesses()
    dtos = [AdAllowanceDTO(business_id=business_id, allowance=allowance.full, used_allowance=allowance.used)
            for business_id, allowance in allowances.items()]
    return jsonify(AdAllowancesDTO(items=dtos))

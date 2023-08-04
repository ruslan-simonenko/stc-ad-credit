from flask import Blueprint, jsonify

from src.auth.auth_bp import auth_role
from src.auth.auth_service import AuthService
from src.carbon_audit.carbon_audit_dto import CarbonAuditDTO, CarbonAuditsGetResponse
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.user.user_types import UserRole

carbon_audit_bp = Blueprint('carbon_audit', __name__, url_prefix='/carbon_audits')


@carbon_audit_bp.route('/user/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.CARBON_AUDITOR)
def get_for_user():
    user_id = AuthService.get_current_user_id_or_throw()
    audits = [CarbonAuditDTO.from_entity(audit) for audit in CarbonAuditService.get_latest_created_by_user(user_id, 50)]
    return jsonify(CarbonAuditsGetResponse(audits=audits))


from flask import Blueprint, jsonify, request

from src.auth.auth_bp import auth_role
from src.auth.auth_service import AuthService
from src.carbon_audit.carbon_audit_dto import CarbonAuditDTO, CarbonAuditAddForm
from src.carbon_audit.carbon_audit_service import CarbonAuditService
from src.user.user_types import UserRole
from src.utils.dto import ResponseWithObjects, ResponseWithObject

carbon_audit_bp = Blueprint('carbon_audit', __name__, url_prefix='/carbon_audits')


@carbon_audit_bp.route('/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.CARBON_AUDITOR)
def get_all():
    audits = [CarbonAuditDTO.from_entity(audit) for audit in CarbonAuditService.get_all()]
    return jsonify(ResponseWithObjects[CarbonAuditDTO](objects=audits))


@carbon_audit_bp.route('/', methods=['post'])
@auth_role(UserRole.CARBON_AUDITOR)
def add():
    form = CarbonAuditAddForm.model_validate(request.get_json())

    audit = CarbonAuditService.add(
        business_id=form.business_id,
        score=form.score,
        report_date=form.report_date,
        report_url=form.report_url,
        creator_id=AuthService.get_current_user_id_or_throw())
    return jsonify(ResponseWithObject[CarbonAuditDTO](object=CarbonAuditDTO.from_entity(audit)))

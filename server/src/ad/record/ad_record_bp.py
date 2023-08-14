from http import HTTPStatus

from flask import Blueprint, jsonify, request

from src.ad.allowance.ad_allowance_service import AdAllowanceService
from src.ad.record.ad_record_dto import AdRecordDTO, AdRecordAddFormDTO, AdRecordsDTO, ErrorResponse
from src.ad.record.ad_record_service import AdRecordService
from src.auth.auth_bp import auth_role
from src.auth.auth_service import AuthService
from src.user.user_types import UserRole

ad_record_bp = Blueprint('ad_record', __name__, url_prefix='/ad-records')


@ad_record_bp.route('/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.AD_MANAGER)
def get_all():
    ad_records = [AdRecordDTO.from_entity(record) for record in AdRecordService.get_all()]
    return jsonify(AdRecordsDTO(records=ad_records))


@ad_record_bp.route('/', methods=['post'])
@auth_role(UserRole.AD_MANAGER)
def add():
    form = AdRecordAddFormDTO.model_validate(request.get_json())

    if AdAllowanceService.get_remaining_allowance(form.business_id) <= 0:
        return jsonify(ErrorResponse(message='Insufficient ad allowance')), HTTPStatus.FORBIDDEN

    record = AdRecordService.add(
        business_id=form.business_id,
        ad_post_url=form.ad_post_url,
        creator_id=AuthService.get_current_user_id_or_throw())
    return jsonify(AdRecordDTO.from_entity(record))

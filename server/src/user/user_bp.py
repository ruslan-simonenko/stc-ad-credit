import email_normalize
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.user.user_dto import UserInfoDTO, UsersGetManageableResponse, UserAddForm, UserAddSuccessfulResponse, \
    UserAddFailedResponse
from src.user.user_service import UserService
from src.user.user_types import UserRole

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/manageable', methods=['get'])
@jwt_required()
def get_manageable_users():
    users = [UserInfoDTO(
        email=user.email,
        name=user.name,
        picture_url=user.picture_url,
        roles=user.roles
    ) for user in UserService.get_users() if UserRole.CARBON_AUDITOR in user.roles]
    return jsonify(UsersGetManageableResponse(users=users))


@user_bp.route('/', methods=['post'])
@jwt_required()
async def add_user():
    form = UserAddForm.model_validate(request.get_json())
    try:
        normalized_email = await normalize_email(form.email)
    except EmailNormalizationError as e:
        return jsonify(UserAddFailedResponse(message=f'Email validation failed: {str(e)}')), 400
    user = UserService.add_user(normalized_email, form.roles)
    return jsonify(UserAddSuccessfulResponse(user=UserInfoDTO(
        email=user.email,
        roles=user.roles
    )))


async def normalize_email(email: str) -> str:
    result = await email_normalize.Normalizer().normalize(email.strip())
    if not result.mx_records:
        # see https://email-normalize.readthedocs.io/en/stable/result.html
        raise EmailNormalizationError('Failed to fetch MX records for this email address')
    return result.normalized_address


class EmailNormalizationError(Exception):
    def __init__(self, message):
        super().__init__(message)

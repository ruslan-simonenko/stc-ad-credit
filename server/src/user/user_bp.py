import email_normalize
from flask import Blueprint, jsonify, request

from src.auth.auth_bp import auth_role
from src.user.user_dto import UserInfoDTO, UsersGetManageableResponse, UserAddForm, UserAddSuccessfulResponse, \
    UserAddFailedResponse
from src.user.user_service import UserService
from src.user.user_types import UserRole

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/manageable', methods=['get'])
@auth_role(UserRole.ADMIN)
def get_manageable_users():
    users = [UserInfoDTO.from_model(user) for user in UserService.get_users() if UserRole.CARBON_AUDITOR in user.roles]
    return jsonify(UsersGetManageableResponse(users=users))


@user_bp.route('/', methods=['post'])
@auth_role(UserRole.ADMIN)
async def add_user():
    form = UserAddForm.model_validate(request.get_json())
    try:
        normalized_email = await normalize_email(form.email)
    except EmailNormalizationError as e:
        return jsonify(UserAddFailedResponse(message=f'Email validation failed: {str(e)}')), 400
    user = UserService.add_user(normalized_email, form.roles)
    return jsonify(UserAddSuccessfulResponse(user=UserInfoDTO.from_model(user)))


async def normalize_email(email: str) -> str:
    result = await email_normalize.Normalizer().normalize(email.strip())
    if not result.mx_records:
        # see https://email-normalize.readthedocs.io/en/stable/result.html
        raise EmailNormalizationError('Failed to fetch MX records for this email address')
    return result.normalized_address


class EmailNormalizationError(Exception):
    def __init__(self, message):
        super().__init__(message)

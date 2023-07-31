import email_normalize
from flask import Blueprint, jsonify, request, abort

from src.auth.auth_bp import auth_role
from src.user.user_dto import UserInfoDTO, UsersGetManageableResponse, UserAddForm, UserOperationSuccessResponse, \
    UserAddFailedResponse, UserUpdateRequest
from src.user.user_service import UserService
from src.user.user_types import UserRole

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/manageable', methods=['get'])
@auth_role(UserRole.ADMIN)
def get_manageable_users():
    users = [UserInfoDTO.from_entity(user) for user in UserService.get_users()
             if (UserRole.CARBON_AUDITOR.value in [role.name for role in user.roles]) or
             (len(user.roles) == 0)]
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
    return jsonify(UserOperationSuccessResponse(user=UserInfoDTO.from_entity(user)))


@user_bp.route('/<int:user_id>', methods=['put'])
@auth_role(UserRole.ADMIN)
async def update_user(user_id):
    update = UserUpdateRequest.model_validate(request.get_json())
    if update.roles is not None:
        user = UserService.set_user_roles(user_id, update.roles)
    else:
        user = UserService.get_user_by_id(user_id)
    return jsonify(UserOperationSuccessResponse(user=UserInfoDTO.from_entity(user)))


async def normalize_email(email: str) -> str:
    result = await email_normalize.Normalizer().normalize(email.strip())
    if not result.mx_records:
        # see https://email-normalize.readthedocs.io/en/stable/result.html
        raise EmailNormalizationError('Failed to fetch MX records for this email address')
    return result.normalized_address


class EmailNormalizationError(Exception):
    def __init__(self, message):
        super().__init__(message)

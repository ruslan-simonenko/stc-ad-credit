import email_normalize
from flask import Blueprint, jsonify, request

from src.auth.auth_bp import auth_role
from src.user.user_dto import UserInfoDTO, UserAddForm, UserUpdateForm
from src.user.user_service import UserService
from src.user.user_types import UserRole
from src.utils.dto import ResponseWithObjects, ErrorResponse, ResponseWithObject

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/manageable', methods=['get'])
@auth_role(UserRole.ADMIN)
def get_manageable_users():
    users = [UserInfoDTO.from_entity(user) for user in UserService.get_users()]
    return jsonify(ResponseWithObjects[UserInfoDTO](objects=users))


@user_bp.route('/', methods=['post'])
@auth_role(UserRole.ADMIN)
async def add_user():
    form = UserAddForm.model_validate(request.get_json())
    try:
        normalized_email = await normalize_email(form.email)
    except EmailNormalizationError as e:
        return jsonify(ErrorResponse(message=f'Email validation failed: {str(e)}')), 400
    user = UserService.add_user(normalized_email, form.roles)
    return jsonify(ResponseWithObject[UserInfoDTO](object=UserInfoDTO.from_entity(user)))


@user_bp.route('/<int:user_id>', methods=['put'])
@auth_role(UserRole.ADMIN)
async def update_user(user_id):
    form = UserUpdateForm.model_validate(request.get_json())
    try:
        if form.email is not None:
            normalized_email = await normalize_email(form.email)
        else:
            normalized_email = None
    except EmailNormalizationError as e:
        return jsonify(ErrorResponse(message=f'Email validation failed: {str(e)}')), 400
    user = UserService.update_user(user_id, email=normalized_email, roles=form.roles)
    return jsonify(ResponseWithObject[UserInfoDTO](object=UserInfoDTO.from_entity(user)))


async def normalize_email(email: str) -> str:
    result = await email_normalize.Normalizer().normalize(email.strip())
    if not result.mx_records:
        # see https://email-normalize.readthedocs.io/en/stable/result.html
        raise EmailNormalizationError('Failed to fetch MX records for this email address')
    return result.normalized_address


class EmailNormalizationError(Exception):
    def __init__(self, message):
        super().__init__(message)

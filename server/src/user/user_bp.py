from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from src.user.user_dto import UserInfoDTO, UsersGetManageableResponse
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

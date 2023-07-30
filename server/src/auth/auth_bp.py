import os
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Any

from flask import Blueprint, request, jsonify
from flask.blueprints import BlueprintSetupState
from flask_jwt_extended import JWTManager
# noinspection PyPackageRequirements
from google.auth.exceptions import GoogleAuthError
# noinspection PyPackageRequirements
from google.auth.transport import requests
# noinspection PyPackageRequirements
from google.oauth2 import id_token
from pydantic import BaseModel

from src.auth.auth_service import AuthService
from src.config import EnvironmentConstantsKeys
from src.user.user_dto import UserInfoDTO
from src.user.user_service import UserService


def setup_auth_with_jwt(state: BlueprintSetupState):
    state.app.config['JWT_SECRET_KEY'] = os.environ[EnvironmentConstantsKeys.JWT_SECRET_KEY]
    state.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
    JWTManager(state.app)


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_bp.record_once(setup_auth_with_jwt)


@dataclass
class LoginRequest:
    credential: str


class LoginResponse(BaseModel):
    user: UserInfoDTO
    access_token: str

    def __hash__(self) -> int:
        return self.user.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LoginResponse):
            return False
        return (self.user == other.user and
                self.access_token == other.access_token)


@dataclass
class LoginError:
    message: str


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        login_request = LoginRequest(**(request.get_json()))
    except (TypeError, ValueError) as e:
        return jsonify(LoginError(f'Invalid request: {str(e)}')), 400
    try:
        google_client_id = os.environ[EnvironmentConstantsKeys.GOOGLE_LOGIN_CLIENT_ID]
    except KeyError as e:
        return jsonify(LoginError(f'Invalid configuration: environment variable {e.args[0]} is not set')), 500
    try:
        id_info: Dict[str, any] = id_token.verify_oauth2_token(login_request.credential, requests.Request(),
                                                               google_client_id, clock_skew_in_seconds=10)
    except (GoogleAuthError, ValueError) as e:
        return jsonify(LoginError(f'Token verification failed: {str(e)}')), 400
    email = id_info['email']
    user = UserService.get_user(email)
    if not user:
        return jsonify(LoginError(f'Not a known user: {email}')), 403
    try:
        google_picture = id_info['picture']
        google_name = id_info['name']
    except KeyError as e:
        return jsonify(LoginError(f'User profile not accessible, field not found: {str(e)}')), 400
    if user.picture_url != google_picture or user.name != google_name:
        user = UserService.update_user(user, avatar_url=google_picture, name=google_name)
    access_token = AuthService.create_access_token(email)
    return jsonify(LoginResponse(
        user=UserInfoDTO.from_model(user),
        access_token=access_token,
    ))


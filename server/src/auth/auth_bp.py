import os
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List

from flask import Blueprint, request, jsonify
from flask.blueprints import BlueprintSetupState
from flask_jwt_extended import JWTManager, create_access_token
# noinspection PyPackageRequirements
from google.auth.exceptions import GoogleAuthError
# noinspection PyPackageRequirements
from google.auth.transport import requests
# noinspection PyPackageRequirements
from google.oauth2 import id_token

from src.auth.auth_service import AuthService
from src.user.user_types import UserRole
from src.user.user_service import UserService
from src.config import EnvironmentConstantsKeys


def setup_auth_with_jwt(state: BlueprintSetupState):
    state.app.config['JWT_SECRET_KEY'] = os.environ[EnvironmentConstantsKeys.JWT_SECRET_KEY]
    state.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
    JWTManager(state.app)


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_bp.record_once(setup_auth_with_jwt)


@dataclass
class LoginRequest:
    credential: str


@dataclass
class LoginResponse:
    email: str
    name: str
    picture_url: str
    access_token: str
    roles: List[UserRole]


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
    try:
        email = id_info['email']
        user_roles = UserService.get_user_roles(email)
        if UserRole.ADMIN not in user_roles:
            return jsonify(LoginError(f'Not a known user: {email}')), 403
        access_token = AuthService.create_access_token(email)
        return jsonify(LoginResponse(
            email=email,
            name=id_info['name'],
            picture_url=id_info['picture'],
            access_token=access_token,
            roles=user_roles,
        ))
    except KeyError as e:
        return jsonify(LoginError(f'User profile not accessible, field not found: {str(e)}')), 400

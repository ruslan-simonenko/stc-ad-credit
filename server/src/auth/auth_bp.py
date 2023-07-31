import asyncio
import os
from dataclasses import dataclass
from datetime import timedelta
from functools import wraps
from typing import Dict, Any

from flask import Blueprint, request, jsonify, abort
from flask.blueprints import BlueprintSetupState
from flask_jwt_extended import JWTManager, verify_jwt_in_request
# noinspection PyPackageRequirements
from google.auth.exceptions import GoogleAuthError
# noinspection PyPackageRequirements
from google.auth.transport import requests
# noinspection PyPackageRequirements
from google.oauth2 import id_token
from pydantic import BaseModel

from src.auth.auth_dto import LoginAsRequest
from src.auth.auth_service import AuthService
from src.config import EnvironmentConstantsKeys
from src.user.user_dto import UserInfoDTO
from src.user.user_service import UserService
from src.user.user_types import UserRole


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
    if user.avatar_url != google_picture or user.name != google_name:
        user = UserService.update_user(user, avatar_url=google_picture, name=google_name)
    access_token = AuthService.create_access_token(email)
    return jsonify(LoginResponse(
        user=UserInfoDTO.from_entity(user),
        access_token=access_token,
    ))


class AuthorizationError(BaseModel):
    message: str


def auth_role(*allowed_roles: UserRole):
    def wrapper(fn):
        def is_authorized() -> bool:
            verify_jwt_in_request()
            user_roles = AuthService.get_roles_from_claims()
            return any(user_role in allowed_roles for user_role in user_roles)

        @wraps(fn)
        def sync_decorator(*args, **kwargs):
            if is_authorized():
                return fn(*args, **kwargs)
            else:
                return jsonify(AuthorizationError(message='Unauthorized')), 403

        @wraps(fn)
        async def async_decorator(*args, **kwargs):
            if is_authorized():
                return await fn(*args, **kwargs)
            else:
                return jsonify(AuthorizationError(message='Unauthorized')), 403

        if asyncio.iscoroutinefunction(fn):
            return async_decorator
        else:
            return sync_decorator

    return wrapper


@auth_bp.route('/login-as', methods=['POST'])
@auth_role(UserRole.ADMIN)
def login_as():
    if os.environ.get(EnvironmentConstantsKeys.APP_ENV, 'prod') not in ['dev', 'test']:
        abort(404)
    login_request = LoginAsRequest.model_validate(request.get_json())
    user = UserService.get_user_by_id(login_request.user_id)
    if not user:
        return jsonify(LoginError(f'User not found: {login_request.user_id}')), 400
    access_token = AuthService.create_access_token(user.email)
    return jsonify(LoginResponse(
        user=UserInfoDTO.from_entity(user),
        access_token=access_token,
    ))

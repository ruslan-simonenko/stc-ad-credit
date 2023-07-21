import os
from dataclasses import dataclass
from typing import Dict

from flask import Blueprint, request, jsonify
# noinspection PyPackageRequirements
from google.auth.exceptions import GoogleAuthError
# noinspection PyPackageRequirements
from google.auth.transport import requests
# noinspection PyPackageRequirements
from google.oauth2 import id_token

auth_bp = Blueprint('login', __name__, url_prefix='/auth')


@dataclass
class LoginRequest:
    credential: str


@dataclass
class LoginResponse:
    email: str
    name: str
    picture_url: str


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
        google_client_id = os.environ['GOOGLE_LOGIN_CLIENT_ID']
        project_manager_email = os.environ['PROJECT_MANAGER_EMAIL']
    except KeyError as e:
        return jsonify(LoginError(f'Invalid configuration: environment variable {e.args[0]} is not set')), 500
    try:
        id_info: Dict[str, any] = id_token.verify_oauth2_token(login_request.credential, requests.Request(),
                                                               google_client_id, clock_skew_in_seconds=10)
    except (GoogleAuthError, ValueError) as e:
        return jsonify(LoginError(f'Token verification failed: {str(e)}')), 400
    try:
        email = id_info['email']
        if email != project_manager_email:
            return jsonify(LoginError(f'Not a known user: {email}')), 403
        return jsonify(LoginResponse(
            email,
            id_info['name'],
            id_info['picture']
        ))
    except KeyError as e:
        return jsonify(LoginError(f'User profile not accessible, field not found: {str(e)}')), 400

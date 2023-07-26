from typing import Dict

from _pytest.monkeypatch import MonkeyPatch
from flask.testing import FlaskClient
# noinspection PyPackageRequirements
from google.oauth2 import id_token

from auth import auth_bp
from auth.auth_bp import LoginRequest
from config import EnvironmentConstantsKeys


def test_login(monkeypatch: MonkeyPatch, client: FlaskClient):
    mock_google_token = 'testcredential'
    mock_google_client_id = 'google_client_id'
    mock_google_response = dict(email='admin@stc.com', name='Admin', picture='')

    mock_access_token = 'mockjwtaccesstoken'

    # noinspection PyUnusedLocal
    def mock_verify_oauth2_token(id_token, request, audience, clock_skew_in_seconds) -> Dict[str, any]:
        assert id_token == mock_google_token
        assert audience == mock_google_client_id
        return mock_google_response

    def mock_create_access_token(identity) -> str:
        return mock_access_token

    monkeypatch.setenv(EnvironmentConstantsKeys.PROJECT_MANAGER_EMAIL, mock_google_response['email'])
    monkeypatch.setenv(EnvironmentConstantsKeys.GOOGLE_LOGIN_CLIENT_ID, mock_google_client_id)
    monkeypatch.setattr(id_token, 'verify_oauth2_token', mock_verify_oauth2_token)
    monkeypatch.setattr(auth_bp, 'create_access_token', mock_create_access_token)

    response = client.post('/auth/login', json=LoginRequest(credential=mock_google_token))
    assert response.status_code == 200
    assert response.json == dict(
        email=mock_google_response['email'],
        name=mock_google_response['name'],
        picture_url=mock_google_response['picture'],
        access_token=mock_access_token,
    )

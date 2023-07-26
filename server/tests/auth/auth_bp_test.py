from typing import Dict

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask.testing import FlaskClient
# noinspection PyPackageRequirements
from google.oauth2 import id_token

from auth import auth_bp
from auth.auth_bp import LoginRequest
from config import EnvironmentConstantsKeys


class TestLogin:
    MOCK_GOOGLE_TOKEN = 'testcredential'
    MOCK_GOOGLE_CLIENT_ID = 'google_client_id'
    MOCK_GOOGLE_RESPONSE = dict(email='admin@stc.com', name='Admin', picture='')

    MOCK_ACCESS_TOKEN = 'mockjwtaccesstoken'

    @pytest.fixture(autouse=True)
    def setup_mocks(self, monkeypatch: MonkeyPatch) -> None:
        # noinspection PyUnusedLocal,PyShadowingNames
        def mock_verify_oauth2_token(id_token, request, audience, clock_skew_in_seconds) -> Dict[str, any]:
            assert id_token == self.MOCK_GOOGLE_TOKEN
            assert audience == self.MOCK_GOOGLE_CLIENT_ID
            return self.MOCK_GOOGLE_RESPONSE

        def mock_create_access_token(identity) -> str:
            return self.MOCK_ACCESS_TOKEN

        monkeypatch.setenv(EnvironmentConstantsKeys.PROJECT_MANAGER_EMAIL, self.MOCK_GOOGLE_RESPONSE['email'])
        monkeypatch.setenv(EnvironmentConstantsKeys.GOOGLE_LOGIN_CLIENT_ID, self.MOCK_GOOGLE_CLIENT_ID)
        monkeypatch.setattr(id_token, 'verify_oauth2_token', mock_verify_oauth2_token)
        monkeypatch.setattr(auth_bp, 'create_access_token', mock_create_access_token)

    def test_successful_login(self, monkeypatch: MonkeyPatch, client: FlaskClient):
        response = client.post('/auth/login', json=LoginRequest(credential=self.MOCK_GOOGLE_TOKEN))

        assert response.status_code == 200
        assert response.json == dict(
            email=self.MOCK_GOOGLE_RESPONSE['email'],
            name=self.MOCK_GOOGLE_RESPONSE['name'],
            picture_url=self.MOCK_GOOGLE_RESPONSE['picture'],
            access_token=self.MOCK_ACCESS_TOKEN,
        )

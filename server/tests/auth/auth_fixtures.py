from typing import Callable, Dict

import pytest

from app import app
from src.auth.auth_service import AuthService
from src.persistence.schema.user import User
from tests.app_fixtures import AppContextFixture
from tests.user.user_fixtures import UserFixtures


class AuthFixtures(UserFixtures, AppContextFixture):
    @pytest.fixture
    def access_headers_for(self) -> Callable[[User], Dict[str, str]]:
        user_id_to_headers: Dict[int, Dict[str, str]] = {}

        def get_access_header_for_user(user: User):
            if user_id_to_headers.get(user.id) is None:
                with app.app_context():
                    access_token = AuthService.create_access_token(user.id)
                headers = {'Authorization': f'Bearer {access_token}'}
                user_id_to_headers[user.id] = headers
            return user_id_to_headers[user.id]

        return get_access_header_for_user

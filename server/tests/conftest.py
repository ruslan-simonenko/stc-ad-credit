import os

import pytest
from flask.testing import FlaskClient

from app import app
from src.config import EnvironmentConstantsKeys

os.environ[EnvironmentConstantsKeys.APP_ENV] = 'test'


@pytest.fixture(scope='session')
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client

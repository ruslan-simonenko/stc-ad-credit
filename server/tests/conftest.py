import pytest
from flask.testing import FlaskClient

from app import app


@pytest.fixture(scope='session')
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client

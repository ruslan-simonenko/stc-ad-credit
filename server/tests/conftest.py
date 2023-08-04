import pytest
from flask.testing import FlaskClient

from app import app


@pytest.fixture
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client

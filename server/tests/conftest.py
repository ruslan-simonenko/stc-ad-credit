import pytest
from _pytest.monkeypatch import MonkeyPatch

from flask.testing import FlaskClient

from app import app
from config import EnvironmentConstantsKeys


@pytest.fixture(scope='session')
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def monkeypatch_session():
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture(autouse=True, scope='session')
def environment(monkeypatch_session: MonkeyPatch) -> None:
    monkeypatch_session.setenv(EnvironmentConstantsKeys.APP_ENV, 'test')

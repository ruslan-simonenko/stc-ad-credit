import pytest

from app import app


class AutoAppContextFixture:
    @pytest.fixture(autouse=True)
    def auto_app_context(self):
        with app.app_context():
            yield

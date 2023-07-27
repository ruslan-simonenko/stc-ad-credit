import pytest
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy import text

from app import app
from src.persistence.schema import db


class DatabaseTest:

    @pytest.fixture(autouse=True, scope='function')
    def isolate_test_db_data_between_tests(self, monkeypatch: MonkeyPatch):
        # According to https://github.com/pallets-eco/flask-sqlalchemy/issues/1171#issue-1603935306
        with app.app_context():
            engines = db.engines
        engine_cleanup = []
        for key, engine in engines.items():
            connection = engine.connect()
            transaction = connection.begin()
            engines[key] = connection
            engine_cleanup.append((key, engine, connection, transaction))
        yield
        for key, engine, connection, transaction in engine_cleanup:
            transaction.rollback()
            connection.close()
            engines[key] = engine


class TestDatabaseIsolationBetweenTests(DatabaseTest):
    """
    Testing that tests are properly isolated and don't pollute test database. If they do one of the tests will fail.
    """

    def test_db_connection_isolation1(self):
        with app.app_context():
            db.session.execute(text('CREATE TABLE IF NOT EXISTS db_isolation_test(id INTEGER PRIMARY KEY);'))
            db.session.execute(text('INSERT INTO db_isolation_test(id) VALUES(1);'))
            db.session.commit()

    def test_db_connection_isolation2(self):
        with app.app_context():
            db.session.execute(text('CREATE TABLE IF NOT EXISTS db_isolation_test(id INTEGER PRIMARY KEY);'))
            db.session.execute(text('INSERT INTO db_isolation_test(id) VALUES(1);'))
            db.session.commit()

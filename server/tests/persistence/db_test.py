import os
from contextlib import contextmanager

from alembic import command
from alembic.config import Config

from app import app
from src.persistence.schema import db
from src.persistence.schema.user import User
from tests.app_fixtures import AutoAppContextFixture


@contextmanager
def alembic_working_directory():
    working_dir = os.getcwd()
    try:
        os.chdir('db_migration')
        yield
    finally:
        os.chdir(working_dir)


class DatabaseTest:

    @staticmethod
    def get_alembic_config() -> Config:
        config = Config('alembic.ini')
        config.attributes['db-migration-engine'] = db.engine
        return config

    @staticmethod
    def setup_method():
        with app.app_context():
            with alembic_working_directory():
                command.upgrade(DatabaseTest.get_alembic_config(), 'head')

    @staticmethod
    def teardown_method():
        with app.app_context():
            db.session.remove()
            with alembic_working_directory():
                command.downgrade(DatabaseTest.get_alembic_config(), 'base')


class TestDatabaseIsolationBetweenTests(DatabaseTest, AutoAppContextFixture):
    """
    Testing that tests are properly isolated and don't pollute test database. If they do one of the tests will fail.
    """

    def test_db_connection_isolation1(self):
        user = User(email='test-user@gmail.com')
        db.session.add(user)
        db.session.commit()

    def test_db_connection_isolation2(self):
        user = User(email='test-user@gmail.com')
        db.session.add(user)
        db.session.commit()

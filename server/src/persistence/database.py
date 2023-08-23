import os

from flask import Blueprint
from flask.blueprints import BlueprintSetupState

from src.config import EnvironmentConstantsKeys
from src.persistence.schema import db


def setup_database(state: BlueprintSetupState):
    app_env = os.environ.get(EnvironmentConstantsKeys.APP_ENV, 'prod')
    if app_env in ['prod', 'dev']:
        user = os.environ[EnvironmentConstantsKeys.DB_USER]
        password = os.environ[EnvironmentConstantsKeys.DB_PASSWORD]
        host = os.environ[EnvironmentConstantsKeys.DB_HOST]
        name = os.environ[EnvironmentConstantsKeys.DB_NAME]
        db_path = f'mysql+pymysql://{user}:{password}@{host}/{name}'
    elif app_env == 'test':
        db_path = 'sqlite:///:memory:'
    else:
        raise ValueError(f'Unsupported {EnvironmentConstantsKeys.APP_ENV}: {app_env}')
    state.app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    state.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 150,  # Must be smaller than MySQL's `SHOW GLOBAL VARIABLES LIKE 'wait_timeout';`
        'pool_pre_ping': True,
    }
    state.app.config['SQLALCHEMY_ECHO'] = True

    @state.app.teardown_request
    def session_commit_on_request_completed(exception=None):
        if exception is None:
            db.session.commit()
        else:
            db.session.rollback()

    db.init_app(state.app)


database_bp = Blueprint('database', __name__)
database_bp.record_once(setup_database)

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
        db_path = f'mysql+mysqlconnector://{user}:{password}@{host}/{name}'
    elif app_env == 'test':
        db_path = 'sqlite:///:memory:'
    else:
        raise ValueError(f'Unsupported {EnvironmentConstantsKeys.APP_ENV}: {app_env}')
    state.app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    state.app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(state.app)


database_bp = Blueprint('database', __name__)
database_bp.record_once(setup_database)

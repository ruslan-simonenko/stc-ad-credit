import os

from flask import Blueprint
from flask.blueprints import BlueprintSetupState

from src.config import EnvironmentConstantsKeys
from src.persistence.schema import db


def setup_database(state: BlueprintSetupState):
    app_env = os.environ.get(EnvironmentConstantsKeys.APP_ENV, 'prod')
    # Flask adds prefix 'instance/' to the filename: https://flask.palletsprojects.com/en/2.3.x/config/#instance-folders
    db_path = f'sqlite:///{app_env}.db' if app_env != 'test' else 'sqlite:///:memory:'
    state.app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    state.app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(state.app)


database_bp = Blueprint('database', __name__)
database_bp.record_once(setup_database)

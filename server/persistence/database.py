import os

from flask import Blueprint
from flask.blueprints import BlueprintSetupState

from config import EnvironmentConstantsKeys
from persistence.schema import db


def setup_database(state: BlueprintSetupState):
    app_env = os.environ.get(EnvironmentConstantsKeys.APP_ENV, 'prod')
    # Flask adds prefix instance/ ¯\_(⊙︿⊙)_/¯ - https://flask.palletsprojects.com/en/2.3.x/config/#instance-folders
    state.app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app_env}.db"
    state.app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(state.app)


database_bp = Blueprint('database', __name__)
database_bp.record_once(setup_database)

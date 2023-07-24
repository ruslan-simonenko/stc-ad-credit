from flask import Blueprint
from flask.blueprints import BlueprintSetupState

from persistence import db


def setup_database(state: BlueprintSetupState):
    # This links to instance/dev.db ¯\_(⊙︿⊙)_/¯ - https://flask.palletsprojects.com/en/2.3.x/config/#instance-folders
    state.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
    db.init_app(state.app)


database_bp = Blueprint('database', __name__)
database_bp.record_once(setup_database)

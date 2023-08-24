import asyncio
import os

from dotenv import load_dotenv
from flask import Flask
from flask.json.provider import DefaultJSONProvider
from pydantic import BaseModel
from sqlalchemy import event, exc

from src.ad.allowance.ad_allowance_bp import ad_allowance_bp
from src.ad.record.ad_record_bp import ad_record_bp
from src.ad.strategy.ad_strategy_bp import ad_strategy_bp
from src.auth.auth_bp import auth_bp
from src.business.business_bp import business_bp
from src.carbon_audit.carbon_audit_bp import carbon_audit_bp
from src.config import EnvironmentConstantsKeys
from src.persistence.database import database_bp
from src.persistence.schema import db
from src.user.user_bp import user_bp
from src.user.user_service import UserService
from src.utils.email import normalize_email

env = os.environ.get(EnvironmentConstantsKeys.APP_ENV)
load_dotenv(f'.env.{env}')
if env != 'test':
    load_dotenv('.env.local')


async def setup_admin():
    with app.app_context():
        admin_email = os.environ.get(EnvironmentConstantsKeys.SETUP_ADMIN_WITH_EMAIL)
        if not admin_email:
            return
        admin_email = await normalize_email(admin_email)
        UserService.setup_admin(admin_email)


class PydanticJSONProvider(DefaultJSONProvider):

    def dumps(self, obj, **kwargs):
        if isinstance(obj, BaseModel):
            return obj.model_dump_json()
        return super().dumps(obj, **kwargs)

    def loads(self, s: str | bytes, **kwargs):
        return super().loads(s, **kwargs)


def configure_app(app_: Flask):
    app_.url_map.strict_slashes = False
    app_.register_blueprint(auth_bp)
    app_.register_blueprint(database_bp)
    app_.register_blueprint(user_bp)
    app_.register_blueprint(business_bp)
    app_.register_blueprint(carbon_audit_bp)
    app_.register_blueprint(ad_record_bp)
    app_.register_blueprint(ad_strategy_bp)
    app_.register_blueprint(ad_allowance_bp)
    app_.json_provider_class = PydanticJSONProvider
    app_.json = PydanticJSONProvider(app_)


def prevent_db_connection_reuse_in_forked_processes():
    """
    Prevents DB connections from the pool from being used in app forks.

    Lswsgi starts the app, and then forks it multiple times according to demand. It is unclear how to add a post-fork
    hook to a child process - os.register_at_fork isn't called by lswsgi.

    Instead, re-checking for every connection according to:
    https://docs.sqlalchemy.org/en/20/core/pooling.html#using-connection-pools-with-multiprocessing-or-os-fork
    """
    with app.app_context():
        engine = db.engine

        @event.listens_for(engine, "connect")
        def connect(dbapi_connection, connection_record):
            connection_record.info["pid"] = os.getpid()

        @event.listens_for(engine, "checkout")
        def checkout(dbapi_connection, connection_record, connection_proxy):
            pid = os.getpid()
            if connection_record.info["pid"] != pid:
                connection_record.dbapi_connection = connection_proxy.dbapi_connection = None
                raise exc.DisconnectionError(
                    "Connection record belongs to pid %s, "
                    "attempting to check out in pid %s" % (connection_record.info["pid"], pid)
                )


app = Flask(__name__)
configure_app(app)
if env == 'prod':
    prevent_db_connection_reuse_in_forked_processes()
asyncio.run(setup_admin())


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

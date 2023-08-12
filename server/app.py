import os

from dotenv import load_dotenv
from flask import Flask
from flask.json.provider import DefaultJSONProvider
from pydantic import BaseModel

from src.ad_record.ad_record_bp import ad_record_bp
from src.auth.auth_bp import auth_bp
from src.business.business_bp import business_bp
from src.carbon_audit.carbon_audit_bp import carbon_audit_bp
from src.config import EnvironmentConstantsKeys
from src.persistence.database import database_bp
from src.user.user_bp import user_bp
from src.user.user_service import UserService

if os.environ.get(EnvironmentConstantsKeys.APP_ENV) == 'test':
    load_dotenv('.env.test')
else:
    load_dotenv('.env.local')


def setup_admin():
    with app.app_context():
        admin_email = os.environ.get(EnvironmentConstantsKeys.SETUP_ADMIN_WITH_EMAIL)
        if admin_email:
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
    app_.json_provider_class = PydanticJSONProvider
    app_.json = PydanticJSONProvider(app_)


app = Flask(__name__)
configure_app(app)
setup_admin()


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

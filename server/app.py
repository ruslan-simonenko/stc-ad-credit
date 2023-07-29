import os

from dotenv import load_dotenv
from flask import Flask

from src.auth.auth_bp import auth_bp
from src.user.user_service import UserService
from src.config import EnvironmentConstantsKeys
from src.domain.domain_bp import domain_bp
from src.persistence.database import database_bp

if os.environ.get(EnvironmentConstantsKeys.APP_ENV) == 'test':
    load_dotenv('.env.test')
else:
    load_dotenv('.env.local')


def setup_admin():
    with app.app_context():
        admin_email = os.environ.get(EnvironmentConstantsKeys.SETUP_ADMIN_WITH_EMAIL)
        if admin_email:
            UserService.setup_admin(admin_email)


app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(database_bp)
app.register_blueprint(domain_bp)
setup_admin()


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

from flask import Blueprint

auth_bp = Blueprint('login', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    return {"userName": "Test User 123"}

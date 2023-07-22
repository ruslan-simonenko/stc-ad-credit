from dataclasses import dataclass

from flask import Blueprint, jsonify

carbon_auditor_bp = Blueprint('carbon-auditor', __name__, url_prefix='/carbon-auditor')


@dataclass
class CarbonAuditor:
    email: str
    name: str
    picture_url: str


@carbon_auditor_bp.route('/', methods=['GET'])
def get():
    return jsonify([
        CarbonAuditor(email='john.doe@gmail.com', name='John Doe',
                      picture_url='https://cdn.quasar.dev/img/avatar4.jpg'),
        CarbonAuditor(email='jane.doe@gmail.com', name='Jane Doe', picture_url='https://cdn.quasar.dev/img/avatar2.jpg')
    ])

from dataclasses import dataclass

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import select

from domain.carbon_auditor.carbon_auditor_schema import CarbonAuditorEntity
from persistence import db

carbon_auditor_bp = Blueprint('carbon-auditor', __name__, url_prefix='/carbon-auditor')


@dataclass
class CarbonAuditor:
    email: str
    name: str
    picture_url: str


@carbon_auditor_bp.route('/', methods=['GET'])
@jwt_required()
def get():
    auditor_entities = db.session.execute(select(CarbonAuditorEntity)).scalars().all()
    return jsonify([
        CarbonAuditor(email=auditor.email, name=auditor.name, picture_url=auditor.picture_url)
        for auditor in auditor_entities
    ])

from dataclasses import dataclass

import email_normalize
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from persistence.schema import CarbonAuditor as CarbonAuditorEntity
from persistence.schema import db

carbon_auditor_bp = Blueprint('carbon-auditor', __name__, url_prefix='/carbon-auditor')


@dataclass
class CarbonAuditor:
    email: str
    name: str
    picture_url: str


@carbon_auditor_bp.route('/', methods=['POST'])
@jwt_required()
async def add():
    try:
        add_auditor_request = CarbonAuditorAddRequest(**(request.get_json()))
    except (TypeError, ValueError) as e:
        return jsonify(CarbonAuditorAddError(f'Invalid request: {str(e)}')), 400
    try:
        normalized_email = await normalize_email(add_auditor_request.email)
    except ValueError as e:
        return jsonify(CarbonAuditorAddError(f'Email validation failed: {str(e)}')), 400
    entity = CarbonAuditorEntity(
        email=normalized_email
    )
    db.session.add(entity)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(CarbonAuditorAddError(f'User is already registered: {normalized_email}')), 400
    return jsonify(CarbonAuditorAddResponse(success=True))


async def normalize_email(email: str) -> str:
    result = await email_normalize.Normalizer().normalize(email.strip())
    if not result.mx_records:
        # see https://email-normalize.readthedocs.io/en/stable/result.html
        raise ValueError('Failed to fetch MX records for this email address')
    return result.normalized_address


@carbon_auditor_bp.route('/', methods=['GET'])
@jwt_required()
def get():
    auditor_entities = db.session.execute(select(CarbonAuditorEntity)).scalars().all()
    return jsonify([
        CarbonAuditor(email=auditor.email, name=auditor.name, picture_url=auditor.picture_url)
        for auditor in auditor_entities
    ])


@dataclass
class CarbonAuditorAddRequest:
    email: str


@dataclass
class CarbonAuditorAddResponse:
    success: bool


@dataclass
class CarbonAuditorAddError:
    message: str

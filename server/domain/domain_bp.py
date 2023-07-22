from flask import Blueprint

from domain.carbon_auditor.carbon_auditor_bp import carbon_auditor_bp

domain_bp = Blueprint('domain', __name__, url_prefix='/domain')
domain_bp.register_blueprint(carbon_auditor_bp)

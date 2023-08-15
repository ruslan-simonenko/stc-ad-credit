from flask import Blueprint, jsonify

from src.ad.strategy.ad_strategy import AD_ALLOWANCE, \
    AD_RATE_LIMIT_WINDOW_DURATION
from src.ad.strategy.ad_strategy_dto import AdStrategyDTO
from src.auth.auth_bp import auth_role
from src.carbon_audit.rating.carbon_audit_rating_service import CARBON_RATING_MIN_SCORE
from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating
from src.user.user_types import UserRole

ad_strategy_bp = Blueprint('ad_strategy', __name__, url_prefix='/ad-strategy')


@ad_strategy_bp.route('/', methods=['get'])
@auth_role(UserRole.ADMIN, UserRole.AD_MANAGER)
def get():
    return jsonify(AdStrategyDTO(
        rating_medium_min_score=CARBON_RATING_MIN_SCORE[CarbonAuditRating.MEDIUM],
        rating_high_min_score=CARBON_RATING_MIN_SCORE[CarbonAuditRating.HIGH],
        ads_allowance_unknown_rating=AD_ALLOWANCE[CarbonAuditRating.UNKNOWN],
        ads_allowance_low_rating=AD_ALLOWANCE[CarbonAuditRating.LOW],
        ads_allowance_medium_rating=AD_ALLOWANCE[CarbonAuditRating.MEDIUM],
        ads_allowance_high_rating=AD_ALLOWANCE[CarbonAuditRating.HIGH],
        ads_allowance_window_days=AD_RATE_LIMIT_WINDOW_DURATION.days,
    ))

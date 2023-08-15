from datetime import timedelta
from typing import Dict

from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating

AD_ALLOWANCE: Dict[CarbonAuditRating, int] = {
    CarbonAuditRating.UNKNOWN: 1,
    CarbonAuditRating.LOW: 2,
    CarbonAuditRating.MEDIUM: 5,
    CarbonAuditRating.HIGH: 10,
}

AD_RATE_LIMIT_WINDOW_DURATION = timedelta(days=72)

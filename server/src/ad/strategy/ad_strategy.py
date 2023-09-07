from datetime import timedelta
from typing import Dict

from src.carbon_audit.rating.carbon_audit_rating_types import CarbonAuditRating

AD_ALLOWANCE: Dict[CarbonAuditRating, int] = {
    CarbonAuditRating.UNKNOWN: 5,
    CarbonAuditRating.LOW: 10,
    CarbonAuditRating.MEDIUM: 20,
    CarbonAuditRating.HIGH: 50,
}

AD_RATE_LIMIT_WINDOW_DURATION = timedelta(days=365)

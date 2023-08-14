from datetime import timedelta
from enum import Enum
from typing import Dict


class CarbonAuditRating(Enum):
    UNKNOWN = 'UNKNOWN'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


CARBON_RATING_MIN_SCORE: Dict[CarbonAuditRating, int] = {
    CarbonAuditRating.MEDIUM: 50,
    CarbonAuditRating.HIGH: 70,
}

AD_ALLOWANCE: Dict[CarbonAuditRating, int] = {
    CarbonAuditRating.UNKNOWN: 1,
    CarbonAuditRating.LOW: 2,
    CarbonAuditRating.MEDIUM: 5,
    CarbonAuditRating.HIGH: 10,
}

AD_RATE_LIMIT_WINDOW_DURATION = timedelta(days=72)

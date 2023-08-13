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
    CarbonAuditRating.UNKNOWN: 5,
    CarbonAuditRating.LOW: 10,
    CarbonAuditRating.MEDIUM: 25,
    CarbonAuditRating.HIGH: 50,
}

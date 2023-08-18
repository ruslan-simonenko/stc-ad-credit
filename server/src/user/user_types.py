from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'Admin'
    AD_MANAGER = 'Ad Manager'
    BUSINESS_MANAGER = 'Business Manager'
    CARBON_AUDITOR = 'Carbon Auditor'

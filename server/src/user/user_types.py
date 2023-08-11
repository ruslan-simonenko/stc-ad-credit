from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'Admin'
    CARBON_AUDITOR = 'Carbon Auditor'
    AD_MANAGER = 'Ad Manager'

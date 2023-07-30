from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'Admin'
    CARBON_AUDITOR = 'Carbon Auditor'

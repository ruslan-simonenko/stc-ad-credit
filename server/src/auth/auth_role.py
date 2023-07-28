from enum import Enum


class AuthRole(str, Enum):
    ADMIN = 'Admin'
    CARBON_AUDITOR = 'Carbon Auditor'

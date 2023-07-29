from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, Optional


class UserRole(str, Enum):
    ADMIN = 'Admin'
    CARBON_AUDITOR = 'Carbon Auditor'


@dataclass(eq=True, frozen=True)
class UserInfo:
    email: str
    roles: Tuple[UserRole, ...]
    name: Optional[str] = field(default=None)
    picture_url: Optional[str] = field(default=None)

from typing import FrozenSet

from pydantic import BaseModel


class AdAllowanceDTO(BaseModel):
    business_id: int
    allowance: int
    used_allowance: int

    def __hash__(self):
        return hash((self.business_id, self.allowance, self.used_allowance))

    def __eq__(self, other):
        if not isinstance(other, AdAllowanceDTO):
            return False
        return (self.business_id == other.business_id and
                self.allowance == other.allowance and
                self.used_allowance == other.used_allowance)


class AdAllowancesDTO(BaseModel):
    items: FrozenSet[AdAllowanceDTO]

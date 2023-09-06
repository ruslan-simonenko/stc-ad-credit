from datetime import datetime

from pydantic import BaseModel


class AdAllowanceDTO(BaseModel):
    business_id: int
    window_start: datetime
    window_end: datetime
    allowance: int
    used_allowance: int

    def __hash__(self):
        return hash((self.business_id, self.window_start, self.window_end, self.allowance, self.used_allowance))

    def __eq__(self, other):
        if not isinstance(other, AdAllowanceDTO):
            return False
        return (self.business_id == other.business_id and
                self.window_start == other.window_start and
                self.window_end == other.window_end and
                self.allowance == other.allowance and
                self.used_allowance == other.used_allowance)

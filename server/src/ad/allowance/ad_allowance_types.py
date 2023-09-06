from datetime import datetime

from pydantic import BaseModel


class AdAllowance(BaseModel):
    window_start: datetime
    full: int
    used: int

    @property
    def remaining(self):
        return self.full - self.used

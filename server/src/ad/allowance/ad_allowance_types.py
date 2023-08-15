from pydantic import BaseModel


class AdAllowance(BaseModel):
    full: int
    used: int

    @property
    def remaining(self):
        return self.full - self.used

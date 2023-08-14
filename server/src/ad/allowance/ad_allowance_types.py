from pydantic import BaseModel


class AdAllowance(BaseModel):
    full: int
    used: int

from pydantic import BaseModel


class LoginAsRequest(BaseModel):
    user_id: int

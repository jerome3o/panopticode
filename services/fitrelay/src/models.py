from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    user_profile: dict

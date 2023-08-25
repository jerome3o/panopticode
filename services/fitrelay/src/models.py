from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str
    user_id: str


class TokenInfo(BaseModel):
    user_id: str
    user_profile: dict
    token_response: TokenResponse
    created: int

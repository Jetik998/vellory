from pydantic import BaseModel


class TokenData(BaseModel):
    username: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

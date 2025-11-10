from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    username: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str

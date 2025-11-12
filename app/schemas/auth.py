from pydantic import BaseModel, EmailStr
from app.enums.tokens import TokenType


class TokenData(BaseModel):
    email: str | None = None


class TokenDataUsername(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: TokenType


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str

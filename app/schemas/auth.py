from pydantic import BaseModel, EmailStr
from app.enums.tokens import TokenType


class TokenData(BaseModel):
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: TokenType


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str


class LoginApi(BaseModel):
    username: str
    password: str

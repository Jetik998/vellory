from pydantic import BaseModel


class Base(BaseModel):
    model_config = {"from_attributes": True}


class User(BaseModel):
    username: str
    email: str
    password: str


class UserRegister(User):
    pass


class UserRegisterResponse(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

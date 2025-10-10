from pydantic import BaseModel


class Base(BaseModel):
    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str
    email: str


class UserRegister(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class UserRegisterResponse(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

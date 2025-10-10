from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserRegisterResponse(BaseModel):
    username: str
    message: str

from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    model_config = {"from_attributes": True}


class UserEmail(BaseModel):
    email: EmailStr


class UserBase(UserEmail):
    username: str
    email: EmailStr


class UserResponse(Base):
    username: str
    email: EmailStr


class UserRegister(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class UserRegisterResponse(BaseModel):
    username: str
    message: str


class AvatarUpdateResponse(BaseModel):
    message: str
    avatar_url: str


class AvatarUpdateResponseWeb(BaseModel):
    message: str


class UserResponseWeb(Base, UserBase):
    pass

from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserResponse(Base):
    username: str
    email: EmailStr


class UserResponseWeb(Base):
    username: str
    email: EmailStr
    avatar: str | None = None


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

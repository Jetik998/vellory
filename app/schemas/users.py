from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    # Позволяет Pydantic читать данные из атрибутов объекта (как у SQLAlchemy моделей), а не только из словарей.
    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserResponse(UserBase):
    pass


class UserResponseWeb(UserBase):
    avatar: str | None = None


class UserRegister(UserBase):
    """
    Схема для регистрации нового пользователя.
    Наследует: username, email из UserBase.
    """

    password: str


class UserInDB(UserBase):
    hashed_password: str


class UserRegisterResponse(BaseModel):
    username: str
    message: str


class AvatarUpdateResponse(BaseModel):
    message: str

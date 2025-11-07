from fastapi import HTTPException, UploadFile
from sqlalchemy import select, exists

from app.core.files import save_avatar_file
from app.core.utils import save_and_refresh
from app.models import User
from app.security.password import get_password_hash
from app.schemas.users import UserIn, UserInDB


# Получить пользователя из базы данных, по username
async def db_get_user(username: str, session):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    db_user = result.scalar_one_or_none()
    return db_user


async def db_user_name_exists(username: str, session) -> bool:
    stmt = select(exists().where(User.username == username))
    result = await session.execute(stmt)
    return result.scalars().first()

async def db_user_email_exists(user_email: str, session) -> bool:
    stmt = select(exists().where(User.email == user_email))
    result = await session.execute(stmt)
    return result.scalars().first()


async def db_add_user(user: UserIn, session):
    hashed_password = get_password_hash(user.password)
    db_user_model = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    db_user = User(**db_user_model.model_dump())
    await save_and_refresh(session, db_user)
    return db_user


async def db_update_user_avatar(file: UploadFile, db_user, session):
    db_user.avatar = await save_avatar_file(db_user.username, file)
    await save_and_refresh(session, db_user)
    return db_user

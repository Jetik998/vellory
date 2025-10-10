from sqlalchemy import select, exists

from app.core.utils import save_and_refresh
from app.models import User
from app.security.password import get_password_hash
from app.shemas.users import UserRegister, UserInDB


# Получить пользователя из базы данных, по username
async def db_get_user(username: str, session):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    db_user = result.scalar_one_or_none()
    return db_user


async def db_user_exists(username: str, session) -> bool:
    stmt = select(exists().where(User.username == username))
    result = await session.execute(stmt)
    user_exists = result.scalars().first()
    return user_exists


async def db_add_user(user: UserRegister, session):
    hashed_password = get_password_hash(user.password)
    db_user_model = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    db_user = User(**db_user_model.model_dump())
    await save_and_refresh(session, db_user)
    return db_user

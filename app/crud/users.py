from sqlalchemy import select, exists

from app.crud.utils import save_and_refresh
from app.dependencies import SessionDep
from app.models import User
from app.security import hash_password
from app.shemas.users import Register


#Получить пользователя из базы данных, по username
async def db_get_user(username: str, session: SessionDep):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    db_user = result.scalar_one_or_none()
    return db_user

async def db_user_exists(username: str, session: SessionDep):
    stmt = select(exists().where(User.username == username))
    result = await session.execute(stmt)
    user_exists = result.scalars().first()
    return user_exists

async def db_add_user(user: Register, session: SessionDep):
    hashed_password = hash_password(user.password)
    user_dict = user.model_dump(exclude={"password"})
    user_dict["hashed_password"] = hashed_password
    db_user = User(**user_dict)
    await save_and_refresh(session, db_user)
    return db_user


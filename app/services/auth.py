from app.crud.users import db_get_user
from app.dependencies import SessionDep
from security.password import verify_password


async def authenticate_user(username: str, password: str, session: SessionDep):
    user = await db_get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

from app.crud.users import db_get_user
from app.api.dependencies import SessionDep
from app.security.password import verify_password


async def authenticate_user(email: str, password: str, session: SessionDep):
    user = await db_get_user(session, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

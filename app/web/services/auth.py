import jwt
from jwt import InvalidTokenError

from app.api.dependencies import SessionDep
from app.core.config import SECRET_KEY, ALGORITHM
from app.crud.users import db_get_user


async def verify_token_cookie(token: str | None, session: SessionDep):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
    except InvalidTokenError:
        return None

    user = await db_get_user(username, session)
    return user

import jwt
from jwt import InvalidTokenError
from app.core.config import SECRET_KEY, ALGORITHM
from app.crud.users import db_get_user


async def verify_token_cookie(
    session,
    token: str | None,
):
    if not token:
        return None
    try:
        print(f"verifying token {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"payload: {payload}")
        email = payload.get("sub")
        print(f"username: {email}")
        if not email:
            return None
    except InvalidTokenError:
        return None

    user = await db_get_user(session, email=email)
    print(f"user:{user}")
    return user

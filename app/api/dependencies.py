import jwt
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.exceptions import NotFoundException, UnauthorizedException
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi_limiter.depends import RateLimiter

from app.core.config import settings
from app.core.database import get_session
from app.crud.users import db_get_user
from app.models.user import User
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)
SessionDep = Annotated[AsyncSession, Depends(get_session)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenDep = Annotated[str | None, Depends(oauth2_scheme)]
rate_limiter = Depends(
    RateLimiter(times=settings.RATE_LIMIT_TIMES, seconds=settings.RATE_LIMIT_SECONDS)
)


async def get_current_user(
    bearer_token: TokenDep,
    session: SessionDep,
    access_token: Annotated[str | None, Cookie()] = None,
):
    token = bearer_token or access_token
    if not token:
        raise UnauthorizedException("Отсутствует access токен.")

    user = await verify_token(token, session)
    if user is None:
        raise NotFoundException("Пользователь не найден.")
    return user


async def verify_token(token, session: SessionDep):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")
        if email is None:
            raise UnauthorizedException("Пользователь не найден.")

        token_data = TokenData(email=email)

    except ExpiredSignatureError:
        raise UnauthorizedException("Срок действия токена истёк.")

    except InvalidTokenError:
        raise UnauthorizedException("Неверный токен доступа.")

    user = await db_get_user(session, email=token_data.email)
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_user_from_refresh_token(
    session: SessionDep,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if not refresh_token:
        raise UnauthorizedException("Отсутствует refresh токен.")

    user = await verify_token(refresh_token, session)
    print(f"DEBUG: Email из токена: {user.email}")  # Добавь это

    if not user:
        raise NotFoundException("Пользователь не найден.")

    return user


RefreshUserDep = Annotated[User, Depends(get_user_from_refresh_token)]

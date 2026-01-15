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
from app.enums.tokens import TokenType
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


async def get_current_user_cookie(
    session: SessionDep,
    token_type: TokenType,
    access_token: Annotated[str | None, Cookie()] = None,
    lenient: bool = False,
):
    if access_token is None:
        if lenient:
            return None
        raise UnauthorizedException("Отсутствует access токен.")

    token_data: TokenData = verify_token_cookie(access_token, token_type, lenient)

    if token_data is None:
        if lenient:
            return None
        raise UnauthorizedException("Неверный тип токена доступа или email.")

    user = await db_get_user(session, email=token_data.email)

    if user is None:
        if lenient:
            return None
        raise NotFoundException("Пользователь не найден.")

    return user


def verify_token_cookie(token, expected_token_type, lenient: bool = False):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        token_type: str | None = payload.get("token_type")

        if email and token_type == expected_token_type:
            token_data = TokenData(email=email)
            return token_data

        return None

    except ExpiredSignatureError:
        if lenient:
            return None
        raise UnauthorizedException(
            f"{expected_token_type} Срок действия токена истёк."
        )

    except InvalidTokenError:
        if lenient:
            return None
        raise UnauthorizedException(f"{expected_token_type} Неверный токен.")


async def user_from_cookie_token_access_lenient(
    session: SessionDep,
    access_token: Annotated[str | None, Cookie()] = None,
):
    return await get_current_user_cookie(
        session, TokenType.ACCESS, access_token, lenient=True
    )


async def user_from_cookie_token_access(
    session: SessionDep,
    access_token: Annotated[str | None, Cookie()] = None,
):
    return await get_current_user_cookie(session, TokenType.ACCESS, access_token)


CurrentUserFromCookieAccess = Annotated[User, Depends(user_from_cookie_token_access)]

CurrentUserFromCookieAccessLenient = Annotated[
    User, Depends(user_from_cookie_token_access_lenient)
]


async def user_from_cookie_token_refresh_lenient(
    session: SessionDep,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    return await get_current_user_cookie(
        session, TokenType.REFRESH, refresh_token, lenient=True
    )


async def user_from_cookie_token_refresh(
    session: SessionDep,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    return await get_current_user_cookie(session, TokenType.REFRESH, refresh_token)


CurrentUserFromCookieRefresh = Annotated[User, Depends(user_from_cookie_token_refresh)]

CurrentUserFromCookieRefreshLenient = Annotated[
    User, Depends(user_from_cookie_token_refresh_lenient)
]

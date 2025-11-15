import jwt
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastcrud.exceptions.http_exceptions import NotFoundException, UnauthorizedException
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.config import SECRET_KEY, ALGORITHM
from app.core.database import get_session
from app.crud.users import db_get_user
from app.enums.tokens import TokenType
from app.models import User
from app.schemas.auth import TokenData, TokenDataUsername

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
SessionDep = Annotated[AsyncSession, Depends(get_session)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep, session: SessionDep):
    user = await verify_token(token, session)
    if user is None:
        raise NotFoundException("User not found.")
    return user


async def verify_token(token, session: SessionDep):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise UnauthorizedException()
        token_data = TokenDataUsername(username=username)

    except ExpiredSignatureError:
        raise UnauthorizedException("Access token has expired.")

    except InvalidTokenError:
        raise UnauthorizedException("Invalid access token.")

    user = await db_get_user(session, username=token_data.username)
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
        raise UnauthorizedException("Access token missing.")

    token_data: TokenData = verify_token_cookie(access_token, token_type, lenient)

    if token_data is None:
        if lenient:
            return None
        raise UnauthorizedException("Invalid access token type or email.")

    user = await db_get_user(session, email=token_data.email)

    if user is None:
        if lenient:
            return None
        raise NotFoundException("User not found.")

    if user.avatar:
        user.avatar = f"avatars/{user.avatar}"

    return user


def verify_token_cookie(token, expected_token_type, lenient: bool = False):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type: str | None = payload.get("token_type")

        if email and token_type == expected_token_type:
            token_data = TokenData(email=email)
            return token_data

        return None

    except ExpiredSignatureError:
        if lenient:
            return None
        raise UnauthorizedException(f"{expected_token_type} token has expired.")

    except InvalidTokenError:
        if lenient:
            return None
        raise UnauthorizedException(f"Invalid {expected_token_type} token.")


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

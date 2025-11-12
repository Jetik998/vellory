import jwt
from fastapi import Depends, Request
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
    request: Request, session: SessionDep, token_type: TokenType
):
    token = request.cookies.get("access_token")

    if token is None:
        raise UnauthorizedException("Access token missing.")

    token_data: TokenData = verify_token_cookie(token, token_type)

    if token_data is None:
        raise UnauthorizedException("Invalid access token type or email.")

    user = await db_get_user(session, email=token_data.email)

    if user is None:
        raise NotFoundException("User not found.")

    return user


def verify_token_cookie(token, expected_token_type):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type: str | None = payload.get("token_type")

        if email and token_type == expected_token_type:
            token_data = TokenData(email=email)
            return token_data

        return None

    except ExpiredSignatureError:
        raise UnauthorizedException(f"{expected_token_type} token has expired.")

    except InvalidTokenError:
        raise UnauthorizedException(f"Invalid {expected_token_type} token.")


async def user_from_cookie_token_access(request: Request, session: SessionDep):
    return await get_current_user_cookie(TokenType.ACCESS, session)


async def user_from_cookie_token_refresh(request: Request, session: SessionDep):
    return await get_current_user_cookie(TokenType.REFRESH, session)


CurrentUserFromCookieAccess = Annotated[User, Depends(user_from_cookie_token_access)]

CurrentUserFromCookieRefresh = Annotated[User, Depends(user_from_cookie_token_refresh)]

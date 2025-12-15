from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.config import settings
from app.enums.tokens import TokenType


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    to_encode.update({"exp": expire, "token_type": TokenType.ACCESS})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_tokens(identity: str) -> dict[str, str]:

    tokens = {
        "access_token": create_access_token(data={"sub": identity}),
        "refresh_token": create_refresh_token(data={"sub": identity}),
    }
    return tokens


def set_tokens(response, tokens) -> dict[str, str]:
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=15).total_seconds()),
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(days=5).total_seconds()),
    )

    return {
        "access_token": "created",
        "refresh_token": "created",
    }


#
# def tokens_response(tokens):
#     access_token = tokens["access_token"]
#     refresh_token = tokens["refresh_token"]
#     return TokenResponse()

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Request
from app.crud.users import (
    db_add_user,
    db_get_user,
    db_update_user_avatar, db_user_email_exists, db_user_name_exists,
)
from app.enums import Tags

from app.security.auth import authenticate_user
from app.schemas.users import UserIn, UserRegisterResponse, AvatarUpdateResponse
from app.schemas.auth import TokenResponse
from app.core.dependencies import SessionDep, FormDataDep, CurrentUserDep
from app.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=[Tags.auth])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserIn, session: SessionDep) -> UserRegisterResponse:
    if await db_user_name_exists(user.username, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        )
    if await db_user_email_exists(str(user.email), session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        )

    await db_add_user(user, session)
    return UserRegisterResponse(
        username=user.username, message="User registered successfully"
    )


@router.post(
    "/token", summary="Вход в систему и выдача токена", response_model=TokenResponse
)
async def login(form_data: FormDataDep, session: SessionDep) -> TokenResponse:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")

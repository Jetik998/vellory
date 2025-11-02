from fastapi import APIRouter, HTTPException, status, UploadFile, File, Request
from app.crud.users import (
    db_user_exists,
    db_add_user,
    db_get_user,
    db_update_user_avatar,
)
from app.enums import Tags

from app.services.auth import authenticate_user
from app.shemas.users import UserIn, UserRegisterResponse, AvatarUpdateResponse
from app.shemas.auth import TokenResponse
from app.core.dependencies import SessionDep, FormDataDep, CurrentUserDep
from app.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=[Tags.auth])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserIn, session: SessionDep) -> UserRegisterResponse:
    if await db_user_exists(user.username, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
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


@router.post(
    "/avatar",
    summary="Загрузка аватара",
    status_code=status.HTTP_201_CREATED,
    response_model=AvatarUpdateResponse,
)
async def upload_avatar(
    request: Request,
    user: CurrentUserDep,
    session: SessionDep,
    file: UploadFile = File(...),
) -> AvatarUpdateResponse:
    base_url = str(request.base_url).rstrip("/")
    db_user = await db_get_user(user.username, session)
    updated_user = await db_update_user_avatar(file, db_user, session)
    return AvatarUpdateResponse(
        message="Avatar updated", avatar_url=f"{base_url}/avatars/{updated_user.avatar}"
    )

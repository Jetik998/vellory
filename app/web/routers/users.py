from fastapi import APIRouter, UploadFile, File
from starlette import status
from app.api.dependencies import SessionDep, CurrentUserFromCookieRefreshLenient
from app.crud.users import db_update_user_avatar
from app.enums import Tags
from app.schemas.users import (
    AvatarUpdateResponseWeb,
    UserResponseWeb,
)

router = APIRouter(prefix="/users", tags=[Tags.web_users])


@router.get(
    "/me",
    summary="Получение текущего пользователя",
    response_model=UserResponseWeb,  # подходящая схема
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    user: CurrentUserFromCookieRefreshLenient,
) -> UserResponseWeb:
    return user


@router.post(
    "/avatar/upload",
    summary="Загрузка аватара",
    status_code=status.HTTP_201_CREATED,
    response_model=AvatarUpdateResponseWeb,
)
async def upload_avatar(
    user: CurrentUserFromCookieRefreshLenient,
    session: SessionDep,
    file: UploadFile = File(...),
) -> AvatarUpdateResponseWeb:
    await db_update_user_avatar(file, user, session)
    return AvatarUpdateResponseWeb(message="Avatar updated")

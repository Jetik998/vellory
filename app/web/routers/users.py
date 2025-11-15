from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette import status
from starlette.responses import FileResponse

from app.api.dependencies import SessionDep, CurrentUserFromCookieRefreshLenient
from app.core.avatars import get_avatar_file
from app.crud.users import db_update_user_avatar
from app.enums import Tags
from app.schemas.users import (
    AvatarUpdateResponseWeb,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=[Tags.web_users])


@router.get(
    "/me",
    summary="Получение текущего пользователя",
    response_model=UserResponse,  # подходящая схема
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    user: CurrentUserFromCookieRefreshLenient,
) -> AvatarUpdateResponseWeb:
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


@router.get(
    "/avatar/get",
    response_class=FileResponse,
)
async def get_avatar(
    user: CurrentUserFromCookieRefreshLenient,
) -> FileResponse:

    # поиск файла по маске
    avatar, media_type = await get_avatar_file(user.username)

    if avatar is None:
        raise HTTPException(status_code=404, detail="Avatar not found")

    return FileResponse(avatar, media_type=media_type)

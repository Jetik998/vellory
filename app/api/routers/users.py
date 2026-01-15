from app.api.dependencies import CurrentUserDep, SessionDep, rate_limiter
from app.crud.users import db_get_user, db_update_user_avatar
from app.enums import Tags
from app.schemas.users import AvatarUpdateResponse, UserResponseWeb
from fastapi import APIRouter, status, UploadFile, File, Request

router = APIRouter(prefix="/api/v1/users", tags=[Tags.api_users])


@router.get(
    "/me",
    dependencies=[rate_limiter],
    summary="Получение текущего пользователя",
    response_model=UserResponseWeb,  # подходящая схема
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    user: CurrentUserDep,
) -> UserResponseWeb:
    return user


@router.post(
    "/upload/avatar",
    dependencies=[rate_limiter],
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
    """
    **Загрузка изображения для аватара пользователя**

    ---

    - Этот эндпоинт позволяет существующему пользователю загрузить или обновить аватар.
    - Система принимает файл изображения и сохраняет в хранилище.
    - После успешной загрузки возвращается URL-адрес, по которому теперь доступно новое изображение аватара.
    - Поддерживаются популярные форматы изображений (JPG, JPEG, PNG, SVG) с ограничением на максимальный размер файла 5 MB.
    """
    base_url = str(request.base_url).rstrip("/")
    db_user = await db_get_user(session, username=user.username)
    updated_user = await db_update_user_avatar(file, db_user, session)
    return AvatarUpdateResponse(
        message="Avatar updated", avatar_url=f"{base_url}/avatars/{updated_user.avatar}"
    )

from app.api.dependencies import CurrentUserDep, SessionDep, rate_limiter
from app.crud.users import db_update_user_avatar
from app.enums import Tags
from app.schemas.users import AvatarUpdateResponse, UserResponseWeb
from fastapi import APIRouter, status, UploadFile, File

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
    "/avatar/upload",
    dependencies=[rate_limiter],
    summary="Загрузка аватара",
    status_code=status.HTTP_201_CREATED,
    response_model=AvatarUpdateResponse,
)
async def upload_avatar(
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
    await db_update_user_avatar(file, user, session)
    return AvatarUpdateResponse(message="Avatar updated")

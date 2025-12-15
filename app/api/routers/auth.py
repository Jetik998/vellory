from fastapi import APIRouter, status

from app.enums import Tags
from app.schemas.users import UserRegister, UserRegisterResponse
from app.schemas.auth import TokensResponse
from app.api.dependencies import SessionDep, FormDataDep
from app.security.jwt import create_tokens
from app.services.auth import get_identity_for_authenticate_user
from app.services.users import register_user

router = APIRouter(prefix="/api/auth", tags=[Tags.api_auth])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserRegister, session: SessionDep) -> UserRegisterResponse:
    """
    **Создание новой учетной записи пользователя**

    ---

    - Этот эндпоинт позволяет новому пользователю зарегистрироваться в системе.
    - Необходимо передать уникальное имя пользователя, корректный email-адрес и пароль.
    - После успешной регистрации в системе создается новый аккаунт.
    """
    return await register_user(user, session)


@router.post(
    "/token", summary="Вход в систему и выдача токена", response_model=TokensResponse
)
async def token(form_data: FormDataDep, session: SessionDep) -> TokensResponse:
    """
    **Аутентификация пользователя и получение токенов доступа**

    ---

    - Этот эндпоинт позволяет существующему пользователю войти в систему.
    - Необходимо передать имя пользователя и пароль, указанные при регистрации.
    - После успешной аутентификации система возвращает два токена.
    - Основной токен доступа (access_token) для работы с API.
    - Токен обновления (refresh_token) для получения новых токенов.
    """
    username = await get_identity_for_authenticate_user(form_data, session)
    tokens = create_tokens(username)
    return TokensResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
    )

from fastapi import APIRouter, status
from starlette.responses import Response

from app.enums import Tags
from app.models import User
from app.schemas.users import UserRegister, UserRegisterResponse
from app.schemas.auth import TokensResponse, Login
from app.api.dependencies import SessionDep, FormDataDep, rate_limiter, CurrentUserDep
from app.security.auth import authenticate_user_flexible
from app.security.jwt import create_tokens, set_tokens
from app.services.users import register_user

router = APIRouter(prefix="/api/v1/auth", tags=[Tags.api_auth])


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
    "/token",
    dependencies=[rate_limiter],
    summary="Получение токенов в ",
    response_model=TokensResponse,
)
async def token(form_data: FormDataDep, session: SessionDep) -> TokensResponse:
    """
    **Получение токена через OAuth 2.0 Password Grant Type**

    ---

    - Этот эндпоинт позволяет получить токены доступа с помощью OAuth 2.0 Password Grant Type.
    - Необходимо передать имя пользователя и пароль.
    - В случае успешной аутентификации возвращаются два токена:
    - **access_token**: Токен доступа, который используется для авторизации запросов.
    - **refresh_token**: Токен обновления, который используется для получения нового access_token, когда текущий токен истечет.
    """
    user: User = await authenticate_user_flexible(form_data, session)
    tokens = create_tokens(user.email)
    return TokensResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
    )


@router.post(
    "/authorize",
    dependencies=[rate_limiter],
    summary="Вход в систему и выдача токенов в cookies",
)
async def authorize(user_data: Login, session: SessionDep):
    """
    ** Авторизация для веб-приложения**

    ---

    - Этот эндпоинт позволяет пользователю войти в систему и получить токены доступа.
    - Для авторизации необходимо передать email и пароль.
    - В случае успешной аутентификации токены (access_token и refresh_token) сохраняются в защищенные httpOnly куки.
    - **access_token**: Токен доступа, который используется для авторизации запросов.
    - **refresh_token**: Токен обновления, который используется для получения нового access_token, когда текущий токен истечет.
    """
    user: User = await authenticate_user_flexible(user_data, session)
    tokens = create_tokens(user.email)
    response = Response(status_code=200)
    set_tokens(response, tokens)
    return response


@router.get(
    "/access",
    dependencies=[rate_limiter],
    summary="Проверка текущей сессии",
)
async def verify_access_token(user: CurrentUserDep):
    """
    **Проверка текущей сессии**

    ---

    - Этот эндпоинт позволяет новому пользователю зарегистрироваться в системе.
    - Необходимо передать уникальное имя пользователя, корректный email-адрес и пароль.
    - После успешной регистрации в системе создается новый аккаунт.
    """
    if user:
        return Response(status_code=200)

    return Response(status_code=401)

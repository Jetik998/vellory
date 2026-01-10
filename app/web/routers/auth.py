from fastapi import APIRouter
from starlette.responses import Response

from app.api.dependencies import (
    SessionDep,
    CurrentUserFromCookieRefreshLenient,
    rate_limiter,
)
from app.api.routers.auth import create_tokens
from app.services.auth import get_identity_for_authenticate_user
from app.enums import Tags
from app.schemas.auth import Login

from app.security.jwt import set_tokens

router = APIRouter(prefix="/auth", tags=[Tags.web_auth])


@router.get(
    "/access",
    dependencies=[rate_limiter],
    summary="Обновление сессии пользователя",
)
async def verify_access_token(
    user: CurrentUserFromCookieRefreshLenient, response: Response
):
    """
    **Проверяет refresh-токен в cookie. Если токен валиден — создаёт access-токен и перенаправляет на /. Иначе перенаправляет на /login.**

    ---

    **Args:**
    - `user` (CurrentUserDep): Текущий пользователь.

    **Returns:**
    - `RedirectResponse`: Редирект на `/` при успешной проверке или на `/login` при ошибке.

    **Raises:**
    - `HTTPException`: 500 — внутренняя ошибка сервера при создании задачи.
    """
    if user:
        return Response(status_code=200)

    return Response(status_code=401)


# @router.get(
#     "/refresh",
#     dependencies=[rate_limiter],
#     summary="Обновление сессии пользователя",
# )
# async def verify_refresh_token(
#     user: CurrentUserFromCookieRefreshLenient, response: Response
# ):
#     """
#     **Проверяет refresh-токен в cookie. Если токен валиден — создаёт access-токен и перенаправляет на /. Иначе перенаправляет на /login.**
#
#     ---
#
#     **Args:**
#     - `user` (CurrentUserDep): Текущий пользователь.
#
#     **Returns:**
#     - `RedirectResponse`: Редирект на `/` при успешной проверке или на `/login` при ошибке.
#
#     **Raises:**
#     - `HTTPException`: 500 — внутренняя ошибка сервера при создании задачи.
#     """
#     if user:
#         tokens = create_tokens(user.email)
#         response = RedirectResponse("/", status_code=303)
#         set_tokens(response, tokens)
#         return response
#
#     return RedirectResponse("/login", status_code=303)


@router.post(
    "/authorize",
    dependencies=[rate_limiter],
    summary="Вход в систему",
)
async def token_cookie(user_data: Login, session: SessionDep):
    """
    **Авторизует пользователя по учетным данным и сохраняет токены в cookie.**

    ---

    **Args:**
    - `user_data` (Login): Данные для входа пользователя (email и пароль).

    **Returns:**
    - `RedirectResponse`: Редирект на `/` при успешной авторизации.

    **Raises:**
    - `HTTPException`: 401 — Неверное имя пользователя или пароль.
    - `HTTPException`: 500 — Внутренняя ошибка сервера.
    """
    email = await get_identity_for_authenticate_user(user_data, session)
    tokens = create_tokens(email)
    response = Response(status_code=200)
    set_tokens(response, tokens)
    return response


# @router.post(
#     "/authorize",
#     dependencies=[rate_limiter],
#     summary="Вход в систему",
# )
# async def token_cookie(user_data: Login, session: SessionDep):
#     """
#     **Авторизует пользователя по учетным данным и сохраняет токены в cookie.**
#
#     ---
#
#     **Args:**
#     - `user_data` (Login): Данные для входа пользователя (email и пароль).
#
#     **Returns:**
#     - `RedirectResponse`: Редирект на `/` при успешной авторизации.
#
#     **Raises:**
#     - `HTTPException`: 401 — Неверное имя пользователя или пароль.
#     - `HTTPException`: 500 — Внутренняя ошибка сервера.
#     """
#     email = await get_identity_for_authenticate_user(user_data, session)
#     tokens = create_tokens(email)
#     response = RedirectResponse("/", status_code=303)
#     set_tokens(response, tokens)
#     return response


@router.post(
    "/logout",
    dependencies=[rate_limiter],
    summary="Выход из системы",
)
async def logout():
    """
    **Сбрасывает авторизацию пользователя, удаляя токены из cookie, и перенаправляет на главную страницу.**

    ---

    **Returns:**
    - `RedirectResponse`: Редирект на `/` после выхода.

    **Raises:**
    - `HTTPException`: 500 — внутренняя ошибка сервера.
    """
    response = Response(status_code=204)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response

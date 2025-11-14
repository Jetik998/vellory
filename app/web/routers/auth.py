from fastapi import APIRouter
from starlette.responses import FileResponse, RedirectResponse, Response

from app.api.dependencies import (
    SessionDep,
    CurrentUserFromCookieAccess,
    CurrentUserFromCookieAccessLenient,
    CurrentUserFromCookieRefreshLenient,
)
from app.api.routers.auth import create_tokens, get_email_for_authenticate_user
from app.core.config import BASE_DIR
from app.enums import Tags
from app.schemas.auth import Login
from app.schemas.users import UserEmail
from app.security.jwt import set_tokens

router = APIRouter(tags=[Tags.web])
WEB_DIR = BASE_DIR / "app" / "web" / "templates"
TEMPLATES = BASE_DIR / WEB_DIR
ICON_DIR = BASE_DIR / "app" / "media" / "img"


@router.get("/favicon.ico")
async def favicon():
    return FileResponse(ICON_DIR / "vellory.svg")


@router.get(
    "/",
    summary="Базовая страница",
    description="",
)
async def root(user: CurrentUserFromCookieAccessLenient):
    """
    Возвращает страницу с формой.
    """
    if user:
        return FileResponse(TEMPLATES / "index.html")

    return RedirectResponse("/refresh", status_code=303)


@router.get(
    "/login",
    summary="Базовая страница",
    description="",
)
async def login(user: CurrentUserFromCookieAccessLenient):
    if user:
        return RedirectResponse("/", status_code=303)

    return FileResponse(TEMPLATES / "login.html")


@router.get(
    "/token",
    summary="Проверка токена",
    description="Проверяет access token",
)
async def verify_access_token(user: CurrentUserFromCookieAccess):
    return user


@router.get(
    "/refresh",
    summary="Вход в систему",
    description="Проверяет учетные данные и устанавливает cookie с токеном доступа.",
)
async def verify_refresh_token(
    user: CurrentUserFromCookieRefreshLenient, response: Response
):
    if user:
        tokens = create_tokens(user.email)
        response = RedirectResponse("/", status_code=303)
        set_tokens(response, tokens)
        return response

    return RedirectResponse("/login", status_code=303)


@router.post(
    "/authorize",
    summary="Вход в систему",
    description="Проверяет учетные данные и устанавливает cookie с токеном доступа.",
)
async def token_cookie(user_data: Login, session: SessionDep):
    """
    Авторизует пользователя и сохраняет токен в cookie.
    """
    email: UserEmail = await get_email_for_authenticate_user(user_data, session)
    tokens = create_tokens(email)
    response = RedirectResponse("/", status_code=303)
    set_tokens(response, tokens)
    return response


@router.post(
    "/logout",
    summary="Выход из системы",
    description="Очищает токен авторизации и выполняет перенаправление на главную страницу.",
)
async def logout():
    """
    Сбрасывает авторизацию пользователя.
    """
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response

    #
    # access_token = tokens["access_token"]
    # refresh_token = tokens["refresh_token"]
    #
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=60 * 60,
    # )
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=60 * 60 * 2,  # 7 дней
    # )
    #
    # return {
    #     "access_token": "created",
    #     "refresh_token": "created",
    # }


# @router.get(
#     "/",
#     summary="Главная страница",
#     description="Возвращает HTML-файл главной страницы, если пользователь авторизован с помощью access_token из cookie.",
# )
# async def home(user: CurrentUserFromCookieAccess):
#     """
#     Возвращает главную страницу приложения для авторизованного пользователя.
#
#     Параметры
#     ----------
#     user : CurrentUserFromCookie
#         Объект пользователя, извлечённый из базы данных.
#         Данные о пользователе получены из access_token, сохранённого в cookie.
#
#     Возвращает
#     -------
#     FileResponse
#         HTML-файл главной страницы при успешной аутентификации.
#
#     Исключения
#     ----------
#     UnauthorizedException
#         Если отсутствует или недействителен токен авторизации.
#     NotFoundException
#         Если пользователь, указанный в токене, не найден в базе данных.
#     """
#     return FileResponse(TEMPLATES / "index.html")

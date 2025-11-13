from fastapi import APIRouter
from starlette.responses import FileResponse, RedirectResponse, Response

from app.api.dependencies import (
    SessionDep,
    CurrentUserFromCookieAccess,
)
from app.api.routers.auth import login
from app.core.config import BASE_DIR
from app.enums import Tags
from app.schemas.auth import Login
from app.schemas.users import UserResponse

router = APIRouter(tags=[Tags.web])
WEB_DIR = BASE_DIR / "app" / "web" / "templates"
TEMPLATES = BASE_DIR / WEB_DIR


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Получение данных текущего пользователя",
    description=(
        "Возвращает информацию об авторизованном пользователе. "
        "Требуется действительный токен доступа."
    ),
)
async def me(
    user: CurrentUserFromCookieAccess,
):
    return


@router.get(
    "/",
    summary="Страница с формой",
    description="",
)
async def form(user: CurrentUserFromCookieAccess):
    """
    Возвращает страницу с формой.
    """
    if user:
        return FileResponse(TEMPLATES / "index.html")

    return FileResponse(TEMPLATES / "login.html")


#
# @router.post(
#     "/refresh",
#     summary="Вход в систему",
#     description="Проверяет учетные данные и устанавливает cookie с токеном доступа.",
#     response_model=TokenResponse,
# )
# async def refresh(user: CurrentUserFromCookieRefresh):
#     user_data = db_obj_to_dict(user)
#     create_refresh_token(user_data)


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


@router.post(
    "/login",
    summary="Вход в систему",
    description="Проверяет учетные данные и устанавливает cookie с токеном доступа.",
)
async def token_cookie(user_data: Login, session: SessionDep, response: Response):
    """
    Авторизует пользователя и сохраняет токен в cookie.
    """
    tokens = await login(user_data, session)

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 2,  # 7 дней
    )

    return {
        "access_token": "created",
        "refresh_token": "created",
    }


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

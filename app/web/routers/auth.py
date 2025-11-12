from fastapi import APIRouter, Request
from starlette.responses import FileResponse, RedirectResponse, Response

from app.api.dependencies import SessionDep, CurrentUserFromCookie
from app.api.routers.auth import login
from app.core.config import BASE_DIR
from app.enums import Tags
from app.schemas.auth import TokenResponse, Login

router = APIRouter(tags=[Tags.web])
WEB_DIR = BASE_DIR / "app" / "web" / "templates"
TEMPLATES = BASE_DIR / WEB_DIR


@router.get(
    "/",
    summary="Главная страница",
    description="Возвращает HTML-файл главной страницы, если пользователь авторизован с помощью access_token из cookie.",
)
async def home(user: CurrentUserFromCookie):
    """
    Возвращает главную страницу приложения для авторизованного пользователя.

    Параметры
    ----------
    user : CurrentUserFromCookie
        Объект пользователя, извлечённый из базы данных.
        Данные о пользователе получены из access_token, сохранённого в cookie.

    Возвращает
    -------
    FileResponse
        HTML-файл главной страницы при успешной аутентификации.

    Исключения
    ----------
    UnauthorizedException
        Если отсутствует или недействителен токен авторизации.
    NotFoundException
        Если пользователь, указанный в токене, не найден в базе данных.
    """
    return FileResponse(TEMPLATES / "index.html")


@router.post(
    "/refresh",
    summary="Вход в систему",
    description="Проверяет учетные данные и устанавливает cookie с токеном доступа.",
    response_model=TokenResponse,
)
async def refresh(request: Request, session: SessionDep):
    pass
    # """
    # Авторизует пользователя и сохраняет токен в cookie.
    # """
    # token = request.cookies.get("access_token")
    # access_token = create_access_token(data={"sub": user.email})
    # refresh_token = create_refresh_token(data={"sub": user.email})


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
    "/token-cookie",
    summary="Вход в систему",
    description="Проверяет учетные данные и устанавливает cookie с токеном доступа.",
    response_model=TokenResponse,
)
async def token_cookie(user_data: Login, session: SessionDep, response: Response):
    """
    Авторизует пользователя и сохраняет токен в cookie.
    """
    access_token = await login(user_data, session)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600,
    )
    return TokenResponse(access_token=access_token, token_type="bearer")

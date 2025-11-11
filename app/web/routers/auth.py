from fastapi import APIRouter, Request
from starlette.responses import FileResponse, RedirectResponse, Response

from app.api.dependencies import SessionDep
from app.api.routers.auth import login
from app.core.config import BASE_DIR
from app.enums import Tags
from app.schemas.auth import TokenResponse, Login
from app.web.services.auth import verify_token_cookie

router = APIRouter(tags=[Tags.web])
WEB_DIR = BASE_DIR / "app" / "web" / "templates"
TEMPLATES = BASE_DIR / WEB_DIR


@router.get(
    "/",
    summary="Главная страница",
    description="Возвращает главную страницу при валидном токене авторизации. Если токен отсутствует или недействителен — отображает страницу входа.",
)
async def home(request: Request, session: SessionDep):
    """
    Проверяет токен авторизации в cookies.
    Если токен есть и подтверждён — возвращает index.html.
    При отсутствии или ошибке токена — возвращает login.html.
    """
    token = request.cookies.get("access_token")
    if not token:
        return FileResponse(TEMPLATES / "login.html")
    user = await verify_token_cookie(session, token)
    if user:
        return FileResponse(TEMPLATES / "index.html")
    return FileResponse(TEMPLATES / "login.html")


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
    print(response)
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

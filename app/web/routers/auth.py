from typing import Annotated

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.dependencies import SessionDep
from app.enums import Tags
from app.schemas.users import UserIn
from app.services.users import register_user

web_router = APIRouter(tags=[Tags.web])
templates = Jinja2Templates(directory="app/web/templates")

UserDep = Annotated[UserIn, Form()]


@web_router.get("/", response_class=HTMLResponse, summary="Добро пожаловать")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@web_router.get(
    "/register", response_class=HTMLResponse, summary="Форма регистрации пользователя"
)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@web_router.get("/login", response_class=HTMLResponse, summary="Вход")
async def register(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@web_router.post(
    "/register", response_class=HTMLResponse, summary="Страница успешной регистрации"
)
async def register_web(
    request: Request,
    session: SessionDep,
    user: UserDep,
):
    try:
        result = await register_user(user, session)
        if result:
            return templates.TemplateResponse("avatar.html", {"request": request})

    except HTTPException as e:

        if e.detail == "User with this username or email already exists":
            message = "Пользователь с таким именем или почтой уже существует"
        else:
            message = "Ошибка регистрации пользователя"

    except Exception as e:
        message = f"Ошибка {e}"

    return templates.TemplateResponse(
        "submit.html", {"request": request, "message": message}
    )

from fastapi import APIRouter
from app.enums import Tags

router = APIRouter(tags=[Tags.web_pages])


# @router.get("/favicon.ico")
# async def favicon():
#     return FileResponse(ICON_DIR / "vellory.svg")


# @router.get(
#     "/",
#     dependencies=[rate_limiter],
#     summary="Базовая страница",
# )
# async def root(user: CurrentUserFromCookieAccessLenient):
#     """
#     **Возвращает главную страницу для авторизованного пользователя или перенаправляет на пропверку refresh токена**
#
#     ---
#
#     **Args:**
#     - `user` (CurrentUserDep): Текущий пользователь.
#
#     **Returns:**
#     - `FileResponse`: HTML-файл `index.html` для авторизованного пользователя.
#     - `RedirectResponse`: Редирект на `/auth/refresh`, если пользователь не авторизован.
#
#     **Raises:**
#     - `HTTPException`: 500 — внутренняя ошибка сервера.
#     """
#     if user:
#         return FileResponse(TEMPLATES / "index.html")
#
#     return RedirectResponse("auth/refresh", status_code=303)
#
#
# @router.get(
#     "/login",
#     dependencies=[rate_limiter],
#     summary="Базовая страница",
# )
# async def login(user: CurrentUserFromCookieAccessLenient):
#     """
#     **Возвращает страницу `login.html` для неавторизованного пользователя или перенаправляет на главную страницу, если пользователь уже авторизован.**
#
#     ---
#
#     **Args:**
#     - `user` (CurrentUserDep): Текущий пользователь.
#
#     **Returns:**
#     - `FileResponse`: HTML-файл `login.html` для неавторизованного пользователя.
#     - `RedirectResponse`: Редирект на `/` для авторизованного пользователя.
#
#     **Raises:**
#     - `HTTPException`: 500 — внутренняя ошибка сервера.
#     """
#     if user:
#         return RedirectResponse("/", status_code=303)
#
#     return FileResponse(TEMPLATES / "login.html")

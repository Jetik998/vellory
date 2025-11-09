from fastapi import APIRouter, Request
from starlette.responses import FileResponse, RedirectResponse

from app.api.dependencies import SessionDep
from app.core.config import BASE_DIR
from app.enums import Tags
from app.web.services.auth import verify_token_cookie

router = APIRouter(tags=[Tags.web])
WEB_DIR = BASE_DIR / "app" / "web" / "templates"
TEMPLATES = BASE_DIR / WEB_DIR


@router.get("/")
async def home(request: Request, session: SessionDep):
    token = request.cookies.get("access_token")
    user = await verify_token_cookie(token, session)
    if user:
        return FileResponse(TEMPLATES / "index.html")
    return FileResponse(TEMPLATES / "login.html")


@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    print(response)
    return response

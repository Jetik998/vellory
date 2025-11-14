from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles
from app.core.database import init_db
from app.core.avatars import AVATAR_DIR
from app.middleware import add_process_time_header
from app.api.main import api_router
from app.web.main import web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    await init_db()
    yield


# Создание FastAPI приложения с lifespan
app = FastAPI(lifespan=lifespan)

app.middleware("http")(add_process_time_header)
app.include_router(api_router)
app.include_router(web_router)


app.mount("/avatars", StaticFiles(directory=AVATAR_DIR), name="avatars")
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
app.mount("/img", StaticFiles(directory="app/media/img"), name="img")

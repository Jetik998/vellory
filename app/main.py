from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles
from app.core.database import init_db
from app.core.files import AVATAR_DIR
from app.middleware import add_process_time_header
from app.routers import tasks, auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    await init_db()
    yield


# Создание FastAPI приложения с lifespan
app = FastAPI(lifespan=lifespan)

app.middleware("http")(add_process_time_header)

# Подключение роутера задач
app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(users.router)

app.mount("/avatars", StaticFiles(directory=AVATAR_DIR), name="avatars")

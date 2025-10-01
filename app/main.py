from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    await init_db()
    yield


# Создание FastAPI приложения с lifespan
app = FastAPI(lifespan=lifespan)

# Подключение роутера задач
app.include_router(tasks_router)
app.include_router(users_router)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from app.routers.tasks import router as tasks_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    await init_db()
    yield


# Создание FastAPI приложения с lifespan
app = FastAPI(lifespan=lifespan)

# Подключение роутера задач
app.include_router(tasks_router)




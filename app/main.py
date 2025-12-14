from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles
from app.core.database import init_db
from app.core.logging import setup_logging, get_logger
from app.core.redis import init_redis, close_redis
from app.middleware import add_process_time_header
from app.api.api_router import api_router
from app.web.web_router import web_router
from fastapi_limiter import FastAPILimiter

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    await init_db()
    await init_redis(app)
    await FastAPILimiter.init(app.state.redis)
    try:
        yield
    finally:
        await close_redis(app)
        await FastAPILimiter.close()


# Создание FastAPI приложения с lifespan
app = FastAPI(lifespan=lifespan)

app.middleware("http")(add_process_time_header)
app.include_router(api_router)
app.include_router(web_router)


app.mount("/avatars", StaticFiles(directory="app/media/avatars"), name="avatars")
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
app.mount("/img", StaticFiles(directory="app/media/img"), name="img")

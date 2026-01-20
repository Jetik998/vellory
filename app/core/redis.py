from typing import Annotated
from fastapi import FastAPI, Request, Depends
from redis.asyncio import Redis
from app.core.config import settings
from app.core.logging import get_logger
from unittest.mock import AsyncMock

logger = get_logger(__name__)


async def init_redis(app: FastAPI, db: int | None = None):
    try:
        redis_url = settings.redis_url

        app.state.redis = Redis.from_url(
            redis_url,
            max_connections=20,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True,
            retry_on_timeout=True,
        )

        await app.state.redis.ping()
        if isinstance(app.state.redis, AsyncMock):
            logger.info("Redis Мокнут")
        logger.info("Подключение к Redis выполнено успешно")

    except Exception as e:
        logger.error(f"Не удалось подключиться к Redis: {e}")
        raise


# Функция для корректного закрытия соединения
async def close_redis(app: FastAPI) -> None:
    if hasattr(app.state, "redis"):
        try:
            redis: Redis = app.state.redis
            await redis.aclose()
            logger.info("Соединение с Redis закрыто")
        except Exception as e:
            logger.error(f"Ошибка при закрытии Redis: {e}")
    else:
        logger.warning("Redis не найден")


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis


RedisDep = Annotated[Redis, Depends(get_redis)]

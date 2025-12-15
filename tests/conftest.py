from typing import Callable, Any

import pytest_asyncio
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text  # noqa
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.db_utils import save_and_refresh
from app.core.redis import init_redis, close_redis
from app.main import app
from app.models import User
from app.models.base import Base
from app.core.database import get_session

DATABASE_URL = settings.test_database_url

app: FastAPI
app.dependency_overrides: dict[Any, Callable]

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)
# Создание фабрики сессий, до ручного коммита данные не применяются
async_session = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(
    autouse=True
)  # Эта фикстура запустится автоматически для каждого теста
async def setup_rate_limiter():
    """Фикстура для инициализации лимитера перед каждым тестом."""
    # Инициализируем FastAPILimiter с новой бд 1 Redis
    await init_redis(app, db=1)
    await FastAPILimiter.init(app.state.redis)
    yield
    # Корректно закрываем соединение после теста
    await close_redis(app)


# Фикстура для создания таблиц перед тестами и удаления после
@pytest_asyncio.fixture(scope="function")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Фикстура для получения тестовой сессии БД
@pytest_asyncio.fixture
async def db_session(setup_database):
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    """Создает тестового пользователя в БД"""
    user = User(
        id=1,
        email="test@example.com",
        username="testuser",
        hashed_password="fake_hashed_password",
        avatar=None,  # можно опустить, т.к. nullable
        tasks=[],  # пустой список, связь будет работать корректно
    )
    user = await save_and_refresh(db_session, user)
    return user


# Фикстура для переопределения зависимостей
@pytest_asyncio.fixture
async def client(db_session: AsyncSession, test_user: User):
    """
    Создает тестовый HTTP клиент с переопределенными зависимостями
    """

    # Переопределяем зависимость для получения сессии БД
    async def override_get_session():
        yield db_session

    # Переопределяем зависимость для получения текущего пользователя
    async def override_get_current_user():
        return test_user

    # Применяем переопределения
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Создаем клиент
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()

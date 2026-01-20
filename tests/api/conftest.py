from typing import Callable, Any
import pytest
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
from tests.utils import create_test_user

DATABASE_URL = settings.test_database_url

app: FastAPI
app.dependency_overrides: dict[Any, Callable]


@pytest.fixture(
    autouse=True
)  # Запускается перед каждым тестом автоматически (autouse=True).
async def setup_rate_limiter():
    """Нужен для того, чтобы каждый тест работал с чисто инициализированным rate-limiter’ом в Redis и корректно освобождал ресурсы после выполнения."""
    # Инициализируем FastAPILimiter с новой бд 1 Redis
    await init_redis(app, db=1)
    await FastAPILimiter.init(app.state.redis)
    yield
    # Корректно закрываем соединение после теста
    await close_redis(app)


@pytest.fixture(
    scope="function"
)  # Перед каждым тестом (scope="function") создаёт новый async-движок БД
async def engine():
    """Создает движок БД для каждого теста."""
    engine = create_async_engine(DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def setup_database(engine):
    """Cоздаёт и удаляет таблицы БД для каждого теста."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(engine, setup_database):
    """Создаёт фабрику сессий и отдает одну асинхронную сессию БД для каждого теста."""
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Создает тестового пользователя в БД для тестов"""
    user = create_test_user()
    user = await save_and_refresh(db_session, user)
    return user


# Фикстура для переопределения зависимостей
@pytest.fixture
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

    # Получаем зависимости из основного кода и подставляем тестовые
    # Получение сессий в эндпоинт пойдет через тестовую бд
    # Например: get_session из основного кода, заменится на override_get_session
    # И эндпоинт получит сессию из тестовой бд
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Создаёт асинхронный HTTP-клиент, который отправляет запросы напрямую в FastAPI-приложение без запуска сервера,
    # чтобы полноценно тестировать эндпоинты внутри процесса.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()

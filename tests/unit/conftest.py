from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis import Redis

from app.api.dependencies import get_current_user, rate_limiter
from app.core.database import get_session
from app.core.redis import get_redis
from app.models import User, Task
from app.main import app


@pytest.fixture
def fake_db():
    return AsyncMock()


@pytest.fixture
def fake_redis():
    return AsyncMock()


@pytest.fixture
def fake_close_redis():
    return AsyncMock()


@pytest.fixture
def fake_limiter():
    return AsyncMock()


@pytest.fixture
async def fake_close(*args, **kwargs):
    return None


@pytest.fixture
async def fake_init(*args, **kwargs):
    return None


async def mock_db_create_task(session, task_data, owner_id):
    # Возвращаем объект Task, который пройдет валидацию (id >= 1)
    return Task(
        id=1,  # Обязательно для схемы ID(ge=1)
        user_task_id=task_data.user_task_id,  # Локальный ID
        user_id=owner_id,  # ID владельца
        title=task_data.title,
        description=task_data.description,
        created_at=datetime.now(),
        completed=False,
        priority=task_data.priority,
    )


@pytest.fixture(autouse=True)
def mock_fastapi_limiter(monkeypatch):
    monkeypatch.setattr("app.main.init_db", AsyncMock())
    monkeypatch.setattr("app.main.init_redis", AsyncMock())
    monkeypatch.setattr("app.main.close_redis", AsyncMock())
    monkeypatch.setattr(FastAPILimiter, "init", AsyncMock())
    monkeypatch.setattr(FastAPILimiter, "close", AsyncMock())
    monkeypatch.setattr("app.api.routers.tasks.db_create_task", mock_db_create_task)


mock_session = AsyncMock()


@pytest.fixture
def get_mock_session():
    yield mock_session


@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def get_fake_user():
    """Создает тестового пользователя в БД"""
    return User(
        id=1,
        email="test@example.com",
        username="testuser",
        hashed_password="fake_hashed_password",
        avatar=None,  # можно опустить, т.к. nullable
        tasks=[],
    )


@pytest.fixture
def fake_rate_limiter():
    async def _mock_limiter(request=None, response=None):
        return None

    return _mock_limiter


@pytest.fixture(autouse=True)
def setup_overrides(get_mock_session, get_fake_user):
    async def skip_limiter(request=None, response=None):
        return None

    app.dependency_overrides[get_session] = lambda: get_mock_session
    app.dependency_overrides[get_current_user] = lambda: get_fake_user
    app.dependency_overrides[RateLimiter] = skip_limiter
    mock_redis = AsyncMock(spec=Redis)
    app.dependency_overrides[get_redis] = lambda: mock_redis
    # Исправленная строка:
    # Если rate_limiter это Depends, берем саму функцию через .dependency
    target = (
        rate_limiter.dependency if hasattr(rate_limiter, "dependency") else rate_limiter
    )
    app.dependency_overrides[target] = lambda: None

    yield

    app.dependency_overrides.clear()

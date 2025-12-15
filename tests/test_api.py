from typing import Callable, Any

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text, select  # noqa
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tasks import db_get_task
from app.main import app
from app.models import User, Task
from app.core.database import get_session


app: FastAPI
app.dependency_overrides: dict[Any, Callable]

prefix = "/api/tasks"


@pytest.mark.asyncio
async def test_create_task_success(client: AsyncClient, test_user, db_session):
    """Тест успешного создания задачи"""

    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": 1,
        "completed": False,
    }

    response = await client.post(prefix + "/create_task", json=task_data)

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert data["completed"] == task_data["completed"]
    assert data["id"] == test_user.id
    assert "id" in data

    # Проверяем, что задача действительно создалась в БД

    task_in_db = await db_get_task(db_session, data["id"], test_user.id)

    assert task_in_db is not None
    assert task_in_db.title == task_data["title"]
    assert task_in_db.id == test_user.id


@pytest.mark.asyncio
async def test_create_task_without_auth(db_session: AsyncSession):
    """Тест создания задачи без аутентификации"""

    # Создаем клиент БЕЗ переопределения зависимости пользователя
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "is_completed": False,
        }

        response = await ac.post("/create_task", json=task_data)

        # Должна вернуться ошибка 401 или 403
        assert response.status_code in [401, 403]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_task_invalid_data(client: AsyncClient):
    """Тест создания задачи с невалидными данными"""

    task_data = {
        "title": "",  # Пустой title
        "description": "Test Description",
    }

    response = await client.post("/create_task", json=task_data)

    # Должна вернуться ошибка валидации (422)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_multiple_tasks(
    client: AsyncClient, test_user: User, db_session: AsyncSession
):
    """Тест создания нескольких задач одним пользователем"""

    tasks_data = [
        {
            "title": "Task 1",
            "description": "Desc 1",
            "priority": "low",
            "is_completed": False,
        },
        {
            "title": "Task 2",
            "description": "Desc 2",
            "priority": "medium",
            "is_completed": True,
        },
        {
            "title": "Task 3",
            "description": "Desc 3",
            "priority": "high",
            "is_completed": False,
        },
    ]

    created_ids = []

    for task_data in tasks_data:
        response = await client.post("/create_task", json=task_data)
        assert response.status_code == 201
        data = response.json()
        created_ids.append(data["id"])
        assert data["owner_id"] == test_user.id

    # Проверяем, что все задачи в БД
    from sqlalchemy import func

    result = await db_session.execute(
        select(func.count(Task.id)).where(Task.owner_id == test_user.id)
    )
    count = result.scalar()

    assert count == len(tasks_data)

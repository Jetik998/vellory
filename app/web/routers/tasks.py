from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status, Query

from app.api.dependencies import (
    SessionDep,
    CurrentUserFromCookieRefreshLenient,
    rate_limiter,
)
from app.core.db_utils import save_and_refresh
from app.crud.tasks import db_create_task, db_get_task, db_delete_task, db_get_all_tasks
from app.enums import Tags
from app.schemas.tasks import ResponseTasks, RequestTask, DeleteTask
from app.services.responses import base_responses_web

router = APIRouter(prefix="/tasks", tags=[Tags.web_tasks])

TaskIdPath = Annotated[
    int,
    Path(title="ID задачи", ge=0, examples=[0, 1, 2]),
]


@router.post(
    "/create_task",
    dependencies=[rate_limiter],
    response_model=ResponseTasks,
    status_code=status.HTTP_201_CREATED,
    response_description="Задача создана",
    summary="Добавить задачу",
    responses=base_responses_web,
)
async def create_task(
    task: RequestTask,
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
):
    """
    **Создание новой задачи для текущего пользователя.**

    ---

    **Данные новой задачи (body parameter):**
    - `title`(**string**, обязательно): **Название задачи**
    - `description`(**string**, опционально): **Подробное описание задачи**
    - `priority`(**integer**, опционально): **Приоритет задачи (0 - без приоритета, 1 - низкий, 2 - средний, 3 - высокий)**
    - `completed`(**boolean**, опционально): **Статус выполнения задачи (по умолчанию **false**)**
    """
    try:
        task = await db_create_task(session, task, owner_id=user.id)
        return task

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{task_id}",
    dependencies=[rate_limiter],
    response_model=ResponseTasks,
    status_code=status.HTTP_200_OK,
    summary="Получить задачу по ID",
)
async def get_task(
    task_id: TaskIdPath,
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
) -> ResponseTasks:
    """
    **Получение задачи по её ID.**

    **Параметры запроса:**
    - `task_id`: Уникальный идентификатор задачи (path parameter)

    **Требования:**
    - Пользователь должен быть аутентифицирован

    **Возвращает:**
    - Созданную задачу со всеми полями

    **Возможные ошибки:**
    - **401**: Пользователь не аутентифицирован
    - **404**: Задача не найдена
    - **422**: Невалидный формат task_id
    - **429**: Превышен лимит запросов
    - **500**: Внутренняя ошибка сервера
    """
    try:
        task = await db_get_task(session, task_id, owner_id=user.id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/",
    dependencies=[rate_limiter],
    response_model=list[ResponseTasks],
    response_description="Все задачи отправлены",
    summary="Получить все задачи",
)
# Получить все задачи
async def get_all_task(
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
    completed: bool | None = Query(
        default=None,
        description="Фильтровать задачи по статусу: выполнено или нет",
    ),
    order_by_created: bool | None = Query(
        default=None,
        description="Сортировать задачи по дате создания",
    ),
):
    # Пытаемся получить задачу, если не найдено возвращаем ошибку, если найдена
    tasks = await db_get_all_tasks(session, completed, order_by_created, user.id)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return tasks


@router.patch(
    "/{task_id}",
    dependencies=[rate_limiter],
    response_model=ResponseTasks,
    status_code=status.HTTP_200_OK,
    response_description="Задача изменена",
    summary="Изменить задачу",
)
async def edit_task(
    task_id: TaskIdPath,
    task: RequestTask,
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
):
    db_task = await db_get_task(session, task_id, user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(db_task, k, v)
    new_task = await save_and_refresh(session, db_task)

    if new_task is None:
        raise HTTPException(status_code=404, detail="New Task not found")

    else:
        return new_task


@router.delete(
    "/{task_id}",
    dependencies=[rate_limiter],
    status_code=status.HTTP_200_OK,
    response_description="Задача удалена",
    summary="Удалить задачу",
)
async def delete_task(
    task_id: TaskIdPath,
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
):
    # Пытаемся получить задачу, если не найдено возвращаем ошибку.
    deleted_task_id = await db_delete_task(session, task_id, owner_id=user.id)
    if deleted_task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return DeleteTask(id=deleted_task_id, success=True)

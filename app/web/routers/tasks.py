from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.api.dependencies import SessionDep, CurrentUserFromCookieRefreshLenient
from app.crud.tasks import db_create_task, db_get_task
from app.enums import Tags
from app.schemas.tasks import TaskResponse, CreateTask

router = APIRouter(prefix="/tasks", tags=[Tags.web_tasks])


@router.post(
    "/create_task",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить задачу",
    response_description="Задача создана",
)
async def create_task(
    task: CreateTask,
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
):
    """
    **Создаёт новую задачу для текущего пользователя.**

    ---

    **Args:**
    - `task` (): Данные новой задачи.
    - `session` (SessionDep): Сессия базы данных.
    - `user` (CurrentUserDep): Текущий авторизованный пользователь.

    **Returns:**
    - `dict`: Ту же задачу из Базы Данных.

    **Raises:**
    - `HTTPException`: 500 — внутренняя ошибка сервера при создании задачи.
    """
    try:
        task = await db_create_task(session, task, owner_id=user.id)
        return task

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить задачу по ID",
)
async def get_task(
    task_id: Annotated[
        int,
        Path(title="ID задачи", ge=0, examples=[0, 1, 2]),
    ],
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
) -> TaskResponse:
    """
    **Возвращает задачу по ID для текущего пользователя.**

    ---

    **Args:**
    - `task_id` (int): Уникальный идентификатор задачи.
    - `session` (SessionDep): Сессия базы данных.
    - `user` (CurrentUserDep): Текущий авторизованный пользователь.

    **Returns:**
    - `TaskResponse`: Объект задачи.

    **Raises:**
    - `HTTPException`: 404 — если задача не найдена.
    """

    task = await db_get_task(session, task_id, owner_id=user.email)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status, Query

from app.api.dependencies import SessionDep, CurrentUserFromCookieRefreshLenient
from app.core.utils import save_and_refresh
from app.crud.tasks import db_create_task, db_get_task, db_delete_task, db_get_all_tasks
from app.enums import Tags
from app.schemas.tasks import TaskResponse, CreateTask

router = APIRouter(prefix="/tasks", tags=[Tags.web_tasks])


@router.post(
    "/create_task",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Задача создана",
    summary="Добавить задачу",
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


@router.get(
    "/",
    response_model=list[TaskResponse],
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
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    response_description="Задача изменена",
    summary="Изменить задачу",
)
async def edit_task(
    task_id: int,
    task: CreateTask,
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
    status_code=status.HTTP_200_OK,
    response_description="Задача удалена",
    summary="Удалить задачу",
)
async def delete_task(
    task_id: int,
    session: SessionDep,
    user: CurrentUserFromCookieRefreshLenient,
):
    # Пытаемся получить задачу, если не найдено возвращаем ошибку.
    deleted_task_id = await db_delete_task(session, task_id, owner_id=user.id)
    if deleted_task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"success": True, "task_id": deleted_task_id}

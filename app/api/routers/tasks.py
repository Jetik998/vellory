from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status, Path

from app.core.utils import save_and_refresh
from app.crud.tasks import (
    db_create_task,
    db_get_task,
    db_delete_task,
    db_get_all_tasks,
    db_update_task,
)
from app.enums import Tags
from app.schemas.tasks import (
    TaskCreate,
    TaskResponse,
    EditTask,
    CreateTaskResponse,
)
from app.api.dependencies import SessionDep, CurrentUserDep

router = APIRouter(prefix="/api/tasks", tags=[Tags.items])


@router.post(
    "/create_task",
    response_model=CreateTaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить задачу",
    response_description="Задача создана",
)
async def create_task(
    task: TaskCreate,
    session: SessionDep,
    user: CurrentUserDep,
):
    """
    **Создаёт новую задачу для текущего пользователя.**

    ---

    **Args:**
    - `task` (TaskCreate): Данные новой задачи.
    - `session` (SessionDep): Сессия базы данных.
    - `user` (CurrentUserDep): Текущий авторизованный пользователь.

    **Returns:**
    - `dict`: Статус выполнения и ID созданной задачи.

    **Raises:**
    - `HTTPException`: 500 — внутренняя ошибка сервера при создании задачи.
    """
    try:
        task = await db_create_task(session, task, owner_id=user.id)
        return {"id": task.id, "success": True}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/deprecated_create_task",
    summary="Этот эндпоинт устарел",
    deprecated=True,  # <--- пометка, что эндпоинт устарел
)
async def deprecated_create_task():
    return {"message": "Этот эндпоинт устарел, используйте новый "}


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
    user: CurrentUserDep,
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

    task = await db_get_task(session, task_id, owner_id=user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/", response_model=list[TaskResponse], summary="Получить все задачи")
# Получить все задачи
async def get_all_task(
    session: SessionDep,
    user: CurrentUserDep,
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


@router.delete("/{task_id}", summary="Удалить задачу", status_code=204)
# Удалить задачу
async def delete_task(task_id: int, session: SessionDep, user: CurrentUserDep):
    # Пытаемся получить задачу, если не найдено возвращаем ошибку.
    deleted_task_id = await db_delete_task(session, task_id, owner_id=user.id)
    if deleted_task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"success": True, "task_id": deleted_task_id}


@router.patch(
    "/task/{task_id}/old",
    summary="Изменить задачу",
    response_model=TaskResponse,
    deprecated=True,
)
async def edit_task_old(
    task: EditTask, task_id: int, session: SessionDep, user: CurrentUserDep
):
    db_task = await db_get_task(session, task_id, user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_task = task.model_dump(exclude_unset=True)
    new_task = await db_update_task(session, task_id, update_task, user.id)
    if new_task is None:
        raise HTTPException(status_code=404, detail="New Task not found")

    else:
        return new_task


@router.patch("/task/{task_id}", summary="Изменить задачу", response_model=TaskResponse)
async def edit_task(
    task: EditTask, task_id: int, session: SessionDep, user: CurrentUserDep
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

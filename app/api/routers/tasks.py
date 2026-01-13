from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status, Path

from app.core.db_utils import save_and_refresh
from app.crud.tasks import (
    db_create_task,
    db_get_task,
    db_delete_task,
    db_get_all_tasks,
    db_update_task,
)
from app.enums import Tags
from app.schemas.tasks import (
    ResponseTasks,
    RequestTask,
)
from app.api.dependencies import SessionDep, CurrentUserDep, rate_limiter
from app.services.responses import base_responses_api

router = APIRouter(prefix="/api/tasks", tags=[Tags.api_tasks])


@router.get("/", response_model=list[ResponseTasks], summary="Получить все задачи")
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
    """
    **Получение всех задач**

    ---

    - Этот эндпоинт позволяет получить список всех задач пользователя.
    - Поддерживает фильтрацию по статусу выполнения, а также сортировку по дате создания.
    - В случае успешного выполнения возвращается массив всех задач пользователя с полной информацией о каждой задачи.
    """
    # Пытаемся получить задачу, если не найдено возвращаем ошибку, если найдена
    tasks = await db_get_all_tasks(session, completed, order_by_created, user.id)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return tasks


@router.post(
    "/",
    dependencies=[rate_limiter],
    response_model=ResponseTasks,
    status_code=status.HTTP_201_CREATED,
    response_description="Задача создана",
    summary="Добавить задачу",
    responses=base_responses_api,
)
async def create_task(
    task: RequestTask,
    session: SessionDep,
    user: CurrentUserDep,
):
    """
    **Создание новой задачи**

    ---

    - Этот эндпоинт позволяет пользователям создать новую задачу.
    - В запросе необходимо указать название задачи, описание, приоритет и статус выполнения.
    - В случае успешного выполнения возвращаются данные созданной задачи с присвоенным ID.
    """
    # try:
    task = await db_create_task(session, task, owner_id=user.id)
    return task

    # except Exception:
    #     raise HTTPException(status_code=500, detail="Internal server error")


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
) -> ResponseTasks:
    """
    **Получение задачи по ID**

    ---

    - Этот эндпоинт позволяет получить полную информацию о задаче по её ID.
    - Может использоваться для просмотра и проверки деталей отдельной задачи.
    - В случае успешного выполнения возвращаются данные задачи, соответствующей указанному ID.
    """

    task = await db_get_task(session, task_id, owner_id=user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete("/{task_id}", summary="Удалить задачу", status_code=204)
# Удалить задачу
async def delete_task(task_id: int, session: SessionDep, user: CurrentUserDep):
    """
    **Удаление задачи**

    ---

    - Этот эндпоинт позволяет удалить задачу по её ID.
    - После успешного удаления задача полностью удаляется из системы.
    - Операция удаления необратима. После удаления восстановить задачу невозможно.
    """
    deleted_task_id = await db_delete_task(session, task_id, owner_id=user.id)
    if deleted_task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"success": True, "task_id": deleted_task_id}


@router.patch(
    "/task/{task_id}", summary="Изменить задачу", response_model=ResponseTasks
)
async def edit_task(
    task: RequestTask, task_id: int, session: SessionDep, user: CurrentUserDep
):
    """
    **Обновление существующей задачи**

    ---

    - Этот эндпоинт позволяет обновить информацию о задаче по её ID.
    - Все поля можно изменять
    - Передавайте только те поля, которые необходимо обновить.
    - В случае успешного выполнения возвращается задача с обновлёнными данными.
    """
    db_task = await db_get_task(session, task_id, user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task.model_dump(exclude_unset=True)
    for k, v in update_data.api_tasks():
        setattr(db_task, k, v)
    new_task = await save_and_refresh(session, db_task)

    if new_task is None:
        raise HTTPException(status_code=404, detail="New Task not found")

    else:
        return new_task


@router.patch(
    "/task/{task_id}/old",
    summary="Этот эндпоинт устарел",
    response_model=ResponseTasks,
    deprecated=True,
)
async def edit_task_old(
    task: RequestTask, task_id: int, session: SessionDep, user: CurrentUserDep
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

from fastapi import APIRouter, HTTPException, Query

from app.crud.tasks import (
    db_add_task,
    db_get_task,
    db_delete_task,
    db_get_all_tasks,
    db_update_task,
)
from app.shemas.tasks import (
    AddTask,
    GetTaskResponse,
    EditTask,
    AddTaskResponse,
    DeleteTaskResponse,
)
from app.core.dependencies import SessionDep, CurrentUserDep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/add_task", summary="Добавить задачу", response_model=AddTaskResponse)
# При отправке post запроса вызывается функция add_task
async def add_task(
    task: AddTask,
    session: SessionDep,
    user: CurrentUserDep,
):
    try:
        task = await db_add_task(session, task, owner_id=user.id)
        return {"success": True, "task_id": task.id}
    except ValueError as e:  # ошибка клиента
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:  # любая другая ошибка
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{task_id}", summary="Получить задачу по id", response_model=GetTaskResponse
)
# Получить задачу
async def get_task(task_id: int, session: SessionDep):
    # Пытаемся получить задачу, если не найдено возвращаем ошибку, если найдена
    task = await db_get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return task


@router.get("/", response_model=list[GetTaskResponse], summary="Получить все задачи")
# Получить все задачи
async def get_all_task(
    session: SessionDep,
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
    tasks = await db_get_all_tasks(session, completed, order_by_created)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return tasks


@router.delete(
    "/{task_id}", summary="Удалить задачу", response_model=DeleteTaskResponse
)
# Удалить задачу
async def delete_task(task_id: int, session: SessionDep):
    # Пытаемся получить задачу, если не найдено возвращаем ошибку.
    deleted_task_id = await db_delete_task(session, task_id)
    if deleted_task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"success": "deleted", "task_id": deleted_task_id}


@router.put(
    "/task/{task_id}", summary="Изменить задачу", response_model=GetTaskResponse
)
async def edit_task(task: EditTask, task_id: int, session: SessionDep):
    db_task = await db_get_task(session, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_task = task.model_dump(exclude_unset=True)
    new_task = await db_update_task(session, task_id, update_task)
    if new_task is None:
        raise HTTPException(status_code=404, detail="New Task not found")

    else:
        return new_task

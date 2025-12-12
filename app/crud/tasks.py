from sqlalchemy import select
from app.core.utils import save_and_refresh, delete_and_commit
from app.models.task import Task
from app.schemas.tasks import RequestTask


# Функция добавления задачи, Создание объекта, добавление в сессию, комит, обновление, возврат id объекта задачи из базы данных
async def db_create_task(session, task: RequestTask, owner_id: int):
    data = task.model_dump()
    db_task = Task(**data, user_id=owner_id)
    await save_and_refresh(session, db_task)
    return db_task


async def db_get_task(session, task_id: int, owner_id: int):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == owner_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


# Удалить объект задачи из базы данных, по id
async def db_delete_task(session, task_id: int, owner_id: int):
    # Получаем строку из БД
    stmt = select(Task).where(Task.id == task_id, Task.user_id == owner_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if task is None:
        return None

    await delete_and_commit(session, task)
    return task_id


async def db_get_all_tasks(session, completed, order_by_created, user_id):
    stmt = select(Task).where(Task.user_id == user_id)

    if order_by_created:
        stmt = stmt.order_by(Task.created_at)
    if completed:
        stmt = stmt.filter(Task.completed == completed)

    result = await session.execute(stmt)
    users = result.scalars().all()  # Список объектов
    return users


async def db_update_task(session, task_id, task, user_id):
    db_task = await db_get_task(session, task_id, user_id)  # Получили задачу по id
    for key, value in task.items():  # Цикл по словарю task из тела запроса
        if value is not None:
            setattr(db_task, key, value)
    await save_and_refresh(session, db_task)
    return db_task

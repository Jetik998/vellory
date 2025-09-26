from sqlalchemy import select
from app.crud.utils import save_and_refresh
from app.models import Task
from app.shemas.tasks import AddTask


# Функция добавления задачи, Создание объекта, добавление в сессию, комит, обновление, возврат id объекта задачи из базы данных
async def db_add_task(session, task: AddTask):
    db_task = Task(**task.model_dump())
    await save_and_refresh(session, db_task)
    return db_task


# Получить объект задачи из базы данных, по id
async def db_get_task(session, task_id: int):
    # Получаем строку из БД
    task = await session.get(Task, task_id)
    # Возвращаем объект
    return task


# Удалить объект задачи из базы данных, по id
async def db_delete_task(session, task_id: int):
    # Получаем строку из БД
    task = await session.get(Task, task_id)
    if task is None:
        return None

    task_id = task.id
    await session.delete(task)
    await session.commit()
    return task_id


async def db_get_all_tasks(session, completed, order_by_created):
    stmt = select(Task)

    if order_by_created:
        stmt = stmt.order_by(Task.created_at)
    if completed:
        stmt = stmt.filter(Task.completed == completed)

    result = await session.execute(stmt)
    users = result.scalars().all()  # Список объектов
    return users


async def db_update_task(session, task_id, task):
    db_task = await db_get_task(session, task_id)  # Получили задачу по id
    for key, value in task.items():  # Цикл по словарю task из тела запроса
        if value is not None:
            setattr(db_task, key, value)
    await save_and_refresh(session, db_task)
    return db_task

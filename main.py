from fastapi import FastAPI, Depends, HTTPException, Query
from contextlib import asynccontextmanager

from crud import db_add_task, db_get_task, db_delete_task, db_get_all_tasks, db_update_task
from database import get_session, init_db
from shemas import AddTask, TaskOut, EditTask


@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)



@app.post("/tasks/add_task", summary="Добавить задачу")
#Добавить задачу
#При отправке post запроса вызывается функция add_task
async def add_task(task: AddTask, session = Depends(get_session)):
    #Фастапи парсит тело запроса task в объект Pydantic(AddTask)
    #session: передаем через Depends функцию которая возвращает одну сессию
    try:
        #Пытаемся добавить задачу, если все ок возвращаем id добавленой задачи, если нет вызываем ошибку
        task = await db_add_task(session, task)
        return {"success": True, "task_id": task.id}
    except ValueError as e:  # ошибка клиента
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:  # любая другая ошибка
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/tasks/{task_id}", response_model=TaskOut, summary="Получить задачу по id")
#Получить задачу
async def get_task(task_id: int, session = Depends(get_session)):
    #Пытаемся получить задачу, если не найдено возвращаем ошибку, если найдена
    task = await db_get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return task
@app.get("/tasks/", response_model=list[TaskOut], summary="Получить все задачи")
#Получить все задачи
async def get_all_task(
        completed: bool|None = Query(
            default=None,
            description="Фильтровать задачи по статусу: выполнено или нет",
        ),
        order_by_created: bool|None = Query(
            default=None,
            description="Сортировать задачи по дате создания",
        ), session = Depends(get_session)):
    #Пытаемся получить задачу, если не найдено возвращаем ошибку, если найдена
    tasks = await db_get_all_tasks(session, completed, order_by_created)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return tasks

@app.delete("/tasks/{task_id}", summary="Удалить задачу")
#Удалить задачу
async def delete_task(task_id: int, session = Depends(get_session)):
    #Пытаемся получить задачу, если не найдено возвращаем ошибку.
    deleted_task_id = await db_delete_task(session, task_id)
    if deleted_task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"success": "deleted", "task_id": deleted_task_id}


@app.put("/task/{task_id}", response_model=TaskOut, summary="Изменить задачу")
async def edit_task(task: EditTask, task_id: int, session = Depends(get_session)):
    db_task = await db_get_task(session, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_task = task.model_dump(exclude_unset=True)
    new_task = await db_update_task(session, task_id, update_task)
    if new_task is None:
        raise HTTPException(status_code=404, detail="New Task not found")

    else:
        return new_task



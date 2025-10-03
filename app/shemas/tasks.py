from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    model_config = {"from_attributes": True}


# Схема добавления задачи
class AddTask(BaseModel):
    title: str
    description: str
    completed: bool | None = None


# Схема ответа добавления задачи
class AddTaskResponse(BaseModel):
    success: bool
    task_id: int


# Схема получения задачи
class GetTask(BaseModel):
    id: int


class GetTaskResponse(Base):
    id: int
    user_id: int
    title: str
    description: str
    completed: bool
    created_at: datetime


# Схема изменения задачи
class EditTask(BaseModel):
    user_id: int | None = None
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


# Схема удаления задачи
class DeleteTask(BaseModel):
    id: int


class DeleteTaskResponse(BaseModel):
    success: bool
    task_id: int

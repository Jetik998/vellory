from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    model_config = {"from_attributes": True}


# Схема добавления задачи
class AddTask(BaseModel):
    user_id: int
    title: str
    description: str
    completed: bool | None = None


# Схема получения задачи
class GetTask(BaseModel):
    id: int


# Схема изменения задачи
class EditTask(BaseModel):
    user_id: int | None = None
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


# Схема удаления задачи
class DeleteTask(BaseModel):
    id: int


class TaskOut(Base):
    id: int
    user_id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

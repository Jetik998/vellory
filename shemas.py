from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    model_config = {
        "from_attributes": True
    }

#Схема добавления задачи
class AddTask(BaseModel):
    title: str
    description: str
    completed: bool | None = None

#Схема получения задачи
class GetTask(BaseModel):
    id: int

#Схема изменения задачи
class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

#Схема удаления задачи
class DeleteTask(BaseModel):
    id: int

class TaskOut(Base):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

class EditTask(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


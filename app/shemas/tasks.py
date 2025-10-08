from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class Base(BaseModel):
    model_config = {"from_attributes": True}


# Схема добавления задачи
class TaskCreate(BaseModel):
    title: Annotated[
        str, Field(..., min_length=1, max_length=100, description="Название задачи")
    ]
    description: Annotated[
        str | None,
        Field(
            default=None, min_length=1, max_length=100, description="Описание задачи"
        ),
    ]
    completed: Annotated[
        bool | None, Field(default=None, description="Статус выполнения")
    ]


# Схема ответа добавления задачи
class CreateTaskResponse(BaseModel):
    success: bool
    task_id: int


# Схема получения задачи
class GetTask(BaseModel):
    id: int


class TaskResponse(Base):
    id: Annotated[int, Field(..., description="ID задачи")]
    title: Annotated[str, Field(..., description="Название задачи")]
    description: Annotated[str, Field(..., description="Описание задачи")]
    completed: Annotated[bool, Field(..., description="Статус выполнения")]
    created_at: Annotated[datetime, Field(..., description="Дата и время создания")]


# Схема изменения задачи
class EditTask(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


# Схема удаления задачи
class DeleteTask(BaseModel):
    id: int


class DeleteTaskResponse(BaseModel):
    success: bool
    task_id: int | None = None

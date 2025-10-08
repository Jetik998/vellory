from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class Base(BaseModel):
    model_config = {"from_attributes": True}


class BaseTask(BaseModel):
    title: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=100,
            description="Название задачи",
            examples=["Купить продукты"],
        ),
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="Описание задачи",
            examples=["Купить молоко, хлеб и яйца в магазине"],
        ),
    ]
    completed: Annotated[
        bool | None,
        Field(default=False, description="Статус выполнения", examples=[True, False]),
    ]


class TaskCreate(BaseTask):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Купить продукты",
                    "description": "Купить молоко, хлеб и яйца в магазине",
                    "completed": False,
                }
            ],
            "x-test-info": "Это тестовое поле. Здесь можно добавлять любые свои данные для экспериментов.",
        }
    }


class TaskResponse(TaskCreate):
    id: Annotated[int, Field(..., ge=1, description="ID задачи", examples=[1])]
    created_at: Annotated[
        datetime,
        Field(
            ..., description="Дата и время создания", examples=["2025-10-08T14:30:00"]
        ),
    ]


# Схема ответа добавления задачи
class CreateTaskResponse(BaseModel):
    success: bool
    task_id: int


# Схема получения задачи
class GetTask(BaseModel):
    id: int


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

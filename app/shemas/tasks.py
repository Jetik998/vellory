from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    model_config = {"from_attributes": True}


class TaskID(BaseModel):
    id: Annotated[int, Field(..., ge=1, description="ID задачи", examples=[1])]


class TaskBase(BaseModel):
    title: str | None = None
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


class TaskCreate(TaskBase):
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


class TaskResponse(TaskID, TaskCreate):
    created_at: Annotated[
        datetime,
        Field(
            ..., description="Дата и время создания", examples=["2025-10-08T14:30:00"]
        ),
    ]


class CreateTaskResponse(TaskID):
    success: bool


class GetTask(TaskID):
    pass


class EditTask(TaskBase):
    pass


class DeleteTask(TaskID):
    pass

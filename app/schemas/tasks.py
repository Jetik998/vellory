from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    model_config = {"from_attributes": True}


class TaskID(BaseModel):
    id: Annotated[int, Field(..., ge=1, description="ID задачи", examples=[1])]


class TaskBase(BaseModel):
    title: Annotated[
        str | None,
        Field(
            # ..., <- Означает что параметр обязателен при валидации
            default=None,
            min_length=0,
            max_length=100,
            description="Название задачи",
            examples=["Купить продукты"],
        ),
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            min_length=0,
            max_length=100,
            description="Описание задачи",
            examples=["Купить молоко, хлеб и яйца в магазине"],
        ),
    ]
    completed: Annotated[
        bool,
        Field(default=False, description="Статус выполнения", examples=[True, False]),
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


class TaskResponse(TaskID, TaskBase):
    created_at: Annotated[
        datetime,
        Field(
            ..., description="Дата и время создания", examples=["2025-10-08T14:30:00"]
        ),
    ]
    priority: Annotated[
        int,
        Field(..., description="Приоритет задачи (0–3)", ge=-1, le=2, examples=[2]),
    ]


class CreateTask(TaskBase):
    priority: Annotated[
        int,
        Field(default=-1, description="Приоритет задачи (-1:2)", examples=[2]),
    ]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Купить продукты",
                    "description": "Купить молоко, хлеб и яйца в магазине",
                    "completed": False,
                    "priority": 1,
                }
            ],
            "x-test-info": "Это тестовое поле. Здесь можно добавлять любые свои данные для экспериментов.",
        }
    }


class CreateTaskResponse(TaskID):
    success: bool


class GetTask(TaskID):
    pass


class EditTask(TaskBase):
    pass


class DeleteTask(TaskID):
    pass

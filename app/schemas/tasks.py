from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


# ==========================
# БАЗОВЫЕ МОДЕЛИ
# ==========================


class ResponseBase(BaseModel):
    model_config = {"from_attributes": True}


class ID(BaseModel):
    id: Annotated[
        int, Field(..., ge=1, description="ID задачи глобальный", examples=[1])
    ]


class UserTaskID(BaseModel):
    user_task_id: Annotated[
        int,
        Field(
            default=0, description="ID задачи конкретного пользователя", examples=[1]
        ),
    ]


class TaskTittle(BaseModel):
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


class TaskDescription(BaseModel):
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


class TaskCreated(BaseModel):
    created_at: Annotated[
        datetime,
        Field(
            ..., description="Дата и время создания", examples=["2025-10-08T14:30:00"]
        ),
    ]


class TaskCompleted(BaseModel):
    completed: Annotated[
        bool,
        Field(default=False, description="Статус выполнения", examples=[True, False]),
    ]


class TaskPriority(BaseModel):
    priority: Annotated[
        int,
        Field(..., description="Приоритет задачи (0–3)", ge=-1, le=2, examples=[2]),
    ]


# ==========================
# Модели для Эндпоинтов
# ==========================

# class BaseTask(TaskTittle, TaskDescription, TaskCompleted):
#     model_config = {
#         "json_schema_extra": {
#             "examples": [
#                 {
#                     "title": "Купить продукты",
#                     "description": "Купить молоко, хлеб и яйца в магазине",
#                     "completed": False,
#                 }
#             ],
#             "x-test-info": "Это тестовое поле. Здесь можно добавлять любые свои данные для экспериментов.",
#         }
#     }


class RequestTask(UserTaskID, TaskTittle, TaskDescription, TaskPriority):
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


class ResponseTasks(
    ID, UserTaskID, TaskTittle, TaskDescription, TaskPriority, TaskCompleted
):
    pass


class DeleteTask(ID):
    success: bool

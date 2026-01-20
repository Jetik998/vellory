import pytest

from tests.models.tasks import Task, TaskResponse

# ================================
# ВАЛИДНЫЕ КЕЙСЫ
# ================================

valid_case = Task(
    user_task_id=1,
    title="Купить продукты",
    description="Купить молоко, хлеб и яйца в магазине",
    completed=True,
    priority=2,
)


@pytest.fixture
def valid_task():
    return TaskResponse(valid_case.to_dict(), 201, "Задача создана")


# Валидный кейс с минимальными полями
valid_case_minimal = Task(
    user_task_id=2, title="Проверка", description=None, completed=False, priority=1
)


@pytest.fixture
def valid_task_minimal():
    return TaskResponse(valid_case_minimal.to_dict(), 201, "Задача создана")


# ================================
# НЕВАЛИДНЫЕ КЕЙСЫ
# ================================

# 1. Ошибка типа: user_task_id должен быть integer
user_task_id_case = Task(
    user_task_id="1",  # строка вместо int
    title="Купить продукты",
    description="Купить молоко, хлеб и яйца в магазине",
    completed=False,
    priority=2,
)


@pytest.fixture
def user_task_id():
    return TaskResponse(
        user_task_id_case.to_dict(), 422, "Input should be a valid integer"
    )

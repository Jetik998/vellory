import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy import text, select  # noqa
from deepdiff import DeepDiff
from app.api.routers.tasks import prefix_api_tasks
from tests.cases.create_task import valid_task, valid_task_minimal, user_task_id  # noqa
from tests.models.tasks import TaskResponse


class TestCreateTask:
    create_task_url = prefix_api_tasks + "/create_task"

    @pytest.mark.parametrize(
        "task_response_fixture",
        ["valid_task", "valid_task_minimal", "user_task_id"],
    )
    async def test_create_task(
        self, client: AsyncClient, test_user, db_session, task_response_fixture, request
    ):
        """Тест успешного создания задачи"""
        print("loop id:", id(asyncio.get_running_loop()))
        task_response: TaskResponse = request.getfixturevalue(task_response_fixture)
        task_data = task_response.task
        status_code = task_response.status_code

        # Отправка POST-запроса для создания задачи
        response = await client.post(self.create_task_url, json=task_data)
        # Проверяем, что запрос завершился успешно и задача создана
        assert response.status_code == status_code

        if status_code == 201:
            # Получаем данные задачи из ответа
            data = response.json()

            # Сравниваем исходные данные задачи с теми, что вернул API
            # ignore_order=True позволяет игнорировать порядок элементов в списках
            # exclude_paths={"root['id']", "root['user_task_id']"} указывает DeepDiff игнорировать эти поля при сравнении:
            diff = DeepDiff(
                task_data,
                data,
                ignore_order=True,
                exclude_paths={"root['id']", "root['user_task_id']"},
            )

            # Если есть различия, выводим их для отладки
            assert diff == {}, f"Данные ответа отличаются от отправленных: {diff}"

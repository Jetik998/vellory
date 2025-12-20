# import schemathesis
# from httpx import AsyncClient
# from hypothesis import settings, HealthCheck
#
# from app.main import app  # ваш FastAPI‑app
#
# schema = schemathesis.openapi.from_asgi("/openapi.json", app=app)
#
#
# @schema.include(operation_id="create_task_api_tasks_create_task_post").parametrize()
# @settings(max_examples=5, suppress_health_check=[HealthCheck.function_scoped_fixture])
# async def test_create_task_schemathesis(case, test_user, db_session):
#     """
#     Тест проверяет эндпоинт создания задачи, используя случайные данные,
#     сгенерированные schemathesis на основе OpenAPI схемы.
#     """
#     async with AsyncClient(base_url="http://test") as ac:
#         # делает запрос и проверяет ответ на соответствие OpenAPI‑схеме,
#         case.call_and_validate()

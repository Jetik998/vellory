import schemathesis
from hypothesis import settings
from app.main import app  # ваш FastAPI‑app


schema = schemathesis.openapi.from_asgi("/openapi.json", app=app)


@schema.include(path="/api/v1/tasks/", method="POST").parametrize()
@settings(max_examples=10)
async def test_create_task_schemathesis(case):
    print("\n--- TEST CASE ---")
    print(f"Path params: {case.path_parameters}")
    print(f"Query params: {case.query}")
    print(f"Body: {case.body}")
    case.call_and_validate()

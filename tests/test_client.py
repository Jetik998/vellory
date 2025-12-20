from app.main import app
import schemathesis

schema = schemathesis.openapi.from_asgi("/openapi.json", app=app)


@schema.include(operation_id="create_task_api_tasks_create_task_post").parametrize()
def test_create_task_schemathesis(case):
    case.call_and_validate()

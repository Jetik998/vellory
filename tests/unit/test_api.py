import schemathesis
from hypothesis import settings
from app.main import app  # ваш FastAPI‑app


schema = schemathesis.openapi.from_asgi("/openapi.json", app=app)


@schema.include(path="/api/tasks/", method="POST").parametrize()
@settings(max_examples=10)
async def test_create_task_schemathesis(case):
    # --- ДОБАВЬТЕ ЭТОТ БЛОК ---
    # print("\n--- TEST CASE ---")
    # print(f"Path params: {case.path_parameters}")
    # print(f"Query params: {case.query}")
    # print(f"Body: {case.body}")
    # --------------------------
    case.call_and_validate()


# class APIWorkflow(schema.as_state_machine()):
#     def setup(self):
#         """Run once at the start of each test scenario."""
#
#     def teardown(self):
#         """Run once at the end of each test scenario."""
#
#     def before_call(self, case):
#         """Modify every request in the sequence."""
#
#     def after_call(self, response, case):
#         """Process every response."""
#
# TestAPI = APIWorkflow.TestCase

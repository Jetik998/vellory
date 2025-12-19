class Task:
    def __init__(
        self,
        task_id=None,
        user_task_id=None,
        title=None,
        description=None,
        priority=None,
        completed=None,
    ):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.user_task_id = user_task_id

    def to_dict(self):
        return vars(self)


class TaskResponse:
    def __init__(self, task: dict, status_code: int = None, status: str = None):
        self.task = task
        self.status = status
        self.status_code = status_code


# from dotdict3 import DotDict
#
# class CreateTaskData:
#     valid_tasks = [
#         {
#             "title": "Test Task",
#             "description": "Test Description",
#             "priority": 1,
#             "completed": False,
#         }
#     ]
#
#     invalid_task = DotDict({
#         "validation_error": {
#             "body": {
#                 "title": "Test Task",
#                 "description": "Test Description",
#                 "priority": 1,
#                 "completed": False,
#             },
#             "error_code": 422,
#
#         }
#     })
#
#
# print(CreateTaskData().invalid_task.validation_error.body)
# print(CreateTaskData().invalid_task.validation_error.error_code)

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

from typing import List, Optional
from datetime import datetime
from src.entity.models import TaskShema, TaskResponseShema


class InMemoryStorage:
    def __init__(self):
        self.tasks: List[TaskResponseShema] = []
        self.task_id_counter = 1

    def get_tasks_count(self) -> int:
        return len(self.tasks)

    def get_tasks(self) -> List[TaskResponseShema]:
        return self.tasks

    def create_task(self, task: TaskShema) -> TaskResponseShema:
        new_task = TaskResponseShema(
            id=self.task_id_counter,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.task_id_counter += 1
        self.tasks.append(new_task)
        return new_task

    def get_task_by_id(self, task_id: int) -> Optional[TaskResponseShema]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, task_data: TaskShema) -> Optional[TaskResponseShema]:
        for task in self.tasks:
            if task.id == task_id:
                task.title = task_data.title
                task.description = task_data.description
                task.is_completed = task_data.is_completed
                task.updated_at = datetime.now()
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return True
        return False


storage = InMemoryStorage()

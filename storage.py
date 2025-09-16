from typing import List, Dict


class InMemoryStorage:
    def __init__(self):
        self.tasks: List[Dict] = []
        self.task_id_counter = 1

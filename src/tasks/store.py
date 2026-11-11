from dataclasses import dataclass, field
from itertools import count


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


@dataclass
class TaskStore:
    _tasks: dict[int, Task] = field(default_factory=dict)
    _ids: count = field(default_factory=lambda: count(1))

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        task = Task(id=next(self._ids), title=title)
        self._tasks[task.id] = task
        return task

    def complete(self, task_id: int) -> Task:
        task = self._tasks[task_id]
        task.done = True
        return task

    def reopen(self, task_id: int) -> Task:
        task = self._tasks[task_id]
        task.done = False
        return task

    def rename(self, task_id: int, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        if task_id not in self._tasks:
            raise KeyError(task_id)
        task = self._tasks[task_id]
        task.title = title
        return task

    def list(self, include_done: bool = True) -> list[Task]:
        return [t for t in self._tasks.values() if include_done or not t.done]

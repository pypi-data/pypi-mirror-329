from typing import Callable, Any, Awaitable
from .core import Task

class TaskHooks:
    def __init__(self):
        self.pre_task_hooks: List[Callable[[Task], Awaitable[None]]] = []
        self.post_task_hooks: List[Callable[[Task], Awaitable[None]]] = []

    def add_pre_task_hook(self, hook: Callable[[Task], Awaitable[None]]) -> None:
        self.pre_task_hooks.append(hook)

    def add_post_task_hook(self, hook: Callable[[Task], Awaitable[None]]) -> None:
        self.post_task_hooks.append(hook)

    async def run_pre_task_hooks(self, task: Task) -> None:
        for hook in self.pre_task_hooks:
            await hook(task)

    async def run_post_task_hooks(self, task: Task) -> None:
        for hook in self.post_task_hooks:
            await hook(task)

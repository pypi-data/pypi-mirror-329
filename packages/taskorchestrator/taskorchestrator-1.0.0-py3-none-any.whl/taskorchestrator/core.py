import asyncio
from typing import Callable, List, Optional, Any
from typing_extensions import Self

class Task:
    def __init__(
        self,
        func: Callable[[], Any],
        depends_on: Optional[List[Self]] = None,
        retries: int = 0,
        timeout: Optional[float] = None,
    ):
        self.func = func
        self.depends_on = depends_on or []
        self.retries = retries
        self.timeout = timeout
        self.result: Any = None

    async def run(self) -> None:
        for attempt in range(self.retries + 1):
            try:
                if self.depends_on:
                    await asyncio.gather(*(task.run() for task in self.depends_on))
                self.result = await asyncio.wait_for(self.func(), timeout=self.timeout)
                break
            except Exception as e:
                if attempt == self.retries:
                    raise e
                print(f"Retrying {self.func.__name__}... (Attempt {attempt + 1})")

class TaskOrchestrator:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_tasks(self, *tasks: Task) -> None:
        self.tasks.extend(tasks)

    async def run(self) -> List[Any]:
        await asyncio.gather(*(task.run() for task in self.tasks))
        return [task.result for task in self.tasks]

    async def run_parallel(self) -> List[Any]:
        independent_tasks = [task for task in self.tasks if not task.depends_on]
        dependent_tasks = [task for task in self.tasks if task.depends_on]

        await asyncio.gather(*(task.run() for task in independent_tasks))
        await asyncio.gather(*(task.run() for task in dependent_tasks))

        return [task.result for task in self.tasks]

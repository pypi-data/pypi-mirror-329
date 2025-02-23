import asyncio
import pytest
from taskorchestrator.core import Task, TaskOrchestrator

@pytest.mark.asyncio
async def test_task_flow():
    async def task1():
        return 1

    async def task2():
        return 2

    flow = TaskOrchestrator()
    task_1 = Task(task1)
    task_2 = Task(task2, depends_on=[task_1])
    flow.add_tasks(task_1, task_2)

    results = await flow.run()
    assert results == [1, 2]

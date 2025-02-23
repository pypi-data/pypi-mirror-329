import asyncio
import pytest
from taskorchestrator.core import Task
from taskorchestrator.hooks import TaskHooks

@pytest.mark.asyncio
async def test_hooks():
    async def task():
        return "task result"

    async def pre_hook(task: Task):
        print(f"Running pre-task hook for {task.func.__name__}")

    async def post_hook(task: Task):
        print(f"Running post-task hook for {task.func.__name__}")

    hooks = TaskHooks()
    hooks.add_pre_task_hook(pre_hook)
    hooks.add_post_task_hook(post_hook)

    task_instance = Task(task)
    await hooks.run_pre_task_hooks(task_instance)
    await task_instance.run()
    await hooks.run_post_task_hooks(task_instance)

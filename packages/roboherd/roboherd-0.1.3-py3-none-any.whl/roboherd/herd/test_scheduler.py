import asyncio
from unittest.mock import AsyncMock

from .scheduler import HerdScheduler


async def test_empty_scheduler_exits():
    scheduler = HerdScheduler(entries=[], connection=AsyncMock())

    await scheduler.run()


async def test_scheduler_runs_with_task_group_exits():
    scheduler = HerdScheduler(entries=[], connection=AsyncMock())

    async with asyncio.TaskGroup() as tg:
        scheduler.create_task(tg)

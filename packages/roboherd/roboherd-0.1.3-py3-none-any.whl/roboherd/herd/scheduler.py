import asyncio
import logging
from dataclasses import dataclass
from typing import List, Tuple

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from fast_depends import inject

from almabtrieb import Almabtrieb

from roboherd.cow import RoboCow, CronEntry

logger = logging.getLogger(__name__)


@dataclass
class HerdScheduler:
    entries: List[Tuple[RoboCow, CronEntry]]
    connection: Almabtrieb

    def create_task(self, task_group: asyncio.TaskGroup):
        if len(self.entries) == 0:
            logger.info("No tasks to schedule")
            return
        task_group.create_task(self.run())

    async def run(self):
        if len(self.entries) == 0:
            return

        scheduler = AsyncIOScheduler()

        for cow, entry in self.entries:
            trigger = CronTrigger.from_crontab(entry.crontab)
            scheduler.add_job(
                inject(entry.func),
                trigger=trigger,
                kwargs={
                    "actor_id": cow.actor_id,
                    "connection": self.connection,
                    "cow": cow,
                },
            )

        scheduler.start()

        while True:
            await asyncio.sleep(60 * 60)

import asyncio
import logging

from typing import List, Tuple
from dataclasses import dataclass, field

from roboherd.cow import RoboCow, CronEntry
from almabtrieb import Almabtrieb

from .manager import HerdManager
from .scheduler import HerdScheduler
from .processor import HerdProcessor

logger = logging.getLogger(__name__)


@dataclass
class RoboHerd:
    name: str = "RoboHerd"
    base_url: str = "http://abel"

    manager: HerdManager = field(default_factory=HerdManager)
    cows: List[RoboCow] = field(default_factory=list)

    async def run(self, connection: Almabtrieb):
        async with connection:
            self.validate(connection)
            await self.startup(connection)
            await self.process(connection)

    async def startup(self, connection: Almabtrieb):
        self.cows = self.manager.existing_cows(connection.information.actors)

        cows_to_create = self.manager.cows_to_create(connection.information.actors)

        for cow_config in cows_to_create:
            logger.info("Creating cow with name %s", cow_config.name)
            cow = cow_config.load()
            result = await connection.create_actor(
                name=f"{self.manager.prefix}{cow_config.name}",
                base_url=self.base_url,
                preferred_username=cow.information.handle,
                profile={"type": "Service"},
                automatically_accept_followers=True,
            )
            cow.actor_id = result.get("id")

            self.cows.append(cow)

        for cow in self.cows:
            await cow.run_startup(connection)

    async def process(self, connection: Almabtrieb):
        async with asyncio.TaskGroup() as tg:
            logger.info("Starting processing tasks")

            processor = HerdProcessor(connection, self.incoming_handlers())
            processor.create_tasks(tg)

            scheduler = HerdScheduler(self.cron_entries(), connection)
            scheduler.create_task(tg)

    def introduce(self, cow: RoboCow):
        self.manager.add_to_herd(cow)

    def validate(self, connection):
        result = connection.information

        logger.info("Got base urls: %s", ",".join(result.base_urls))

        if self.base_url not in result.base_urls:
            logger.error(
                "Configure base url %s not in base urls %s of server",
                self.base_url,
                ", ".join(result.base_urls),
            )
            raise ValueError("Incorrectly configured base url")

    def cron_entries(self) -> List[Tuple[RoboCow, CronEntry]]:
        """Returns the cron entries of all cows"""

        result = []
        for cow in self.cows:
            for cron_entry in cow.cron_entries:
                result.append((cow, cron_entry))

        return result

    def incoming_handlers(self) -> List[RoboCow]:
        result = []
        for cow in self.cows:
            if cow.handlers.has_handlers:
                result.append(cow)
        return result

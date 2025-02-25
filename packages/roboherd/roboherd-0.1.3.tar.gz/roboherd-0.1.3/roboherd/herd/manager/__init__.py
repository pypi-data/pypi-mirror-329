import logging

from typing import List
from dataclasses import dataclass, field

from almabtrieb.model import ActorInformation

from roboherd.cow import RoboCow

from .config import HerdConfig, CowConfig

logger = logging.getLogger(__name__)


@dataclass
class HerdManager:
    prefix: str = "bot:"
    herd_config: HerdConfig = field(default_factory=HerdConfig)

    @staticmethod
    def from_settings(settings):
        return HerdManager(herd_config=HerdConfig.from_settings(settings))

    def existing_cows(self, actors: List[ActorInformation]) -> List[RoboCow]:
        existing_cows = []

        for info in actors:
            if info.name.startswith(self.prefix):
                cow_name = info.name.removeprefix(self.prefix)
                cow_config = self.herd_config.for_name(cow_name)
                if cow_config:
                    cow = cow_config.load()
                    cow.actor_id = info.id
                    existing_cows.append(cow)

        return existing_cows

    def cows_to_create(self, existing_actors: list[ActorInformation]) -> set[CowConfig]:
        existing_names = {
            actor.name.removeprefix(self.prefix)
            for actor in existing_actors
            if actor.name.startswith(self.prefix)
        }
        names_to_create = self.herd_config.names - existing_names

        return {self.herd_config.for_name(name) for name in names_to_create}

import logging

from typing import Callable
from dataclasses import dataclass
from collections import defaultdict
from almabtrieb import Almabtrieb

from .util import call_handler, HandlerInformation

logger = logging.getLogger(__name__)


@dataclass
class HandlerConfiguration:
    action: str
    activity_type: str
    func: Callable | None = None


class Handlers:
    def __init__(self):
        self.handler_map = defaultdict(lambda: defaultdict(list))

    @property
    def has_handlers(self):
        return len(self.handler_map) > 0

    def add_handler(self, config: HandlerConfiguration, func):
        self.handler_map[config.action][config.activity_type].append(
            HandlerInformation(func=func)
        )

    async def handle(
        self,
        data: dict,
        event_type: str,
        connection: Almabtrieb,
        actor_id: str | None = None,
        cow=None,
    ):
        activity = data.get("data", {}).get("raw", {})
        data_activity_type = activity.get("type")

        if actor_id is None:
            logger.warning("Skipping handlers due to missing actor_id")
            return

        for action in [event_type, "*"]:
            for activity_type in [data_activity_type, "*"]:
                handlers = self.handler_map[action][activity_type]
                for handler_info in handlers:
                    await call_handler(
                        handler_info, data, connection, actor_id=actor_id, cow=cow
                    )

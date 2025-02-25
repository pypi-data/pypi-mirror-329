from fast_depends import inject

from dataclasses import dataclass
from typing import Callable, Dict, Awaitable

from almabtrieb import Almabtrieb


@dataclass
class HandlerInformation:
    func: Callable[[Dict], Awaitable[None]]


async def call_handler(
    handler_info: HandlerInformation,
    data: dict,
    connection: Almabtrieb,
    actor_id: str,
    cow=None,
):
    return await inject(handler_info.func)(
        data=data, connection=connection, actor_id=actor_id, cow=cow
    )

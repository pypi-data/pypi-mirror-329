from unittest.mock import AsyncMock
from almabtrieb.mqtt import MqttConnection

from .util import HandlerInformation, call_handler


async def test_call_handler():
    test_data = {"test": "data"}

    async def func(data: dict):
        assert data == test_data

    handler_info = HandlerInformation(func=func)

    connection = AsyncMock(MqttConnection)

    await call_handler(handler_info, test_data, connection, "actor_id")

import pytest

from unittest.mock import AsyncMock

from almabtrieb.mqtt import MqttConnection

from .handlers import Handlers, HandlerConfiguration


@pytest.mark.parametrize(
    "action,activity_type",
    [
        ("incoming", "AnimalSound"),
        ("incoming", "*"),
        ("*", "AnimalSound"),
        ("*", "*"),
    ],
)
async def test_handlers_should_run(action, activity_type):
    handlers = Handlers()
    connection = AsyncMock(MqttConnection)

    mock = AsyncMock()

    handlers.add_handler(
        HandlerConfiguration(action=action, activity_type=activity_type), mock
    )
    await handlers.handle(
        {"data": {"raw": {"type": "AnimalSound"}}},
        "incoming",
        connection,
        actor_id="actor_id",
    )

    mock.assert_awaited_once()


@pytest.mark.parametrize(
    "action,activity_type",
    [
        ("outgoing", "AnimalSound"),
        ("outgoing", "*"),
        ("*", "Create"),
        ("incoming", "Create"),
    ],
)
async def test_handlers_should_nod_run(action, activity_type):
    handlers = Handlers()
    connection = AsyncMock(MqttConnection)

    mock = AsyncMock()

    handlers.add_handler(
        HandlerConfiguration(action=action, activity_type=activity_type), mock
    )

    await handlers.handle(
        {"data": {"raw": {"type": "AnimalSound"}}},
        "incoming",
        connection,
        actor_id="actor_id",
    )

    mock.assert_not_awaited()


def test_has_handlers():
    handlers = Handlers()

    assert not handlers.has_handlers

    handlers.add_handler(
        HandlerConfiguration(action="outgoing", activity_type="Create"), AsyncMock()
    )

    assert handlers.has_handlers

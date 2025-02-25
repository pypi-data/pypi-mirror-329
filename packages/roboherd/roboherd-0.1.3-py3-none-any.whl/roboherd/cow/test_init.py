import pytest
from unittest.mock import AsyncMock

from . import RoboCow
from .types import Information


@pytest.mark.parametrize(
    "name,summary,profile,expected",
    [
        ("moocow", None, None, True),
        ("moocow", None, {"id": "123"}, True),
        ("moocow", None, {"id": "123", "name": "moocow"}, False),
        ("moocow", None, {"id": "123", "name": "other"}, True),
        ("moocow", "description", {"id": "123", "name": "moocow"}, True),
        (
            "moocow",
            "description",
            {"id": "123", "name": "moocow", "summary": "description"},
            False,
        ),
    ],
)
def test_needs_update(name, summary, profile, expected):
    info = Information(
        handle="testcow",
        name=name,
        description=summary,
    )
    cow = RoboCow(information=info, profile=profile)

    assert cow.needs_update() == expected


def test_cron():
    info = Information(handle="testcow")
    cow = RoboCow(information=info)

    @cow.cron("* * * * *")
    async def test_func():
        pass

    assert len(cow.cron_entries) == 1


async def test_startup():
    info = Information(handle="testcow")
    cow = RoboCow(information=info)
    cow.profile = {"id": "http://host.test/actor/cow"}
    mock = AsyncMock()

    cow.startup(mock)

    await cow.run_startup(AsyncMock())

    mock.assert_called_once()

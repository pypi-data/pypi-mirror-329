import pytest

from roboherd.examples.moocow import moocow
from roboherd.examples.rooster import bot
from roboherd.examples.dev_null import bot as dev_null

from roboherd.cow import CronEntry

from . import RoboHerd


@pytest.mark.parametrize("cow, length", [(moocow, 0), (bot, 1)])
def test_cron_entries(cow, length):
    manager = RoboHerd(cows=[cow])

    assert len(manager.cron_entries()) == length


def test_cron_entries_result():
    manager = RoboHerd(cows=[bot])

    result = manager.cron_entries()[0]

    assert result[0] == bot
    assert isinstance(result[1], CronEntry)


def test_incoming_handlers_no_result():
    manager = RoboHerd(cows=[dev_null])

    assert len(manager.incoming_handlers()) == 0


def test_incoming_handlers_result():
    manager = RoboHerd(cows=[moocow])

    assert len(manager.incoming_handlers()) == 1

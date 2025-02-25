import pytest
from dynaconf import Dynaconf

from almabtrieb.model import ActorInformation


from . import HerdManager


@pytest.fixture
def test_config():
    config = Dynaconf()
    config.update(
        {
            "cow": {
                "moocow": {
                    "bot": "roboherd.examples.moocow:moocow",
                },
                "rooster": {
                    "bot": "roboherd.examples.rooster:bot",
                },
            },
        }
    )
    return config


@pytest.mark.parametrize(
    "actor_info,result_lenth",
    [
        ([], 2),
        ([ActorInformation(name="bot:moocow", id="http://host.test/actor")], 1),
        ([ActorInformation(name="moocow", id="http://host.test/actor")], 2),
        ([ActorInformation(name="bot:other", id="http://host.test/actor")], 2),
    ],
)
def test_cows_to_create(test_config, actor_info, result_lenth):
    manager = HerdManager.from_settings(test_config)

    result = manager.cows_to_create(actor_info)

    assert len(result) == result_lenth

import pytest

from dynaconf import Dynaconf

from roboherd.cow import RoboCow

from .config import CowConfig, HerdConfig


@pytest.fixture
def test_config():
    config = Dynaconf()
    config.update(
        {
            "cow": {
                "moocow": {
                    "bot": "moocow:bot",
                },
                "rooster": {
                    "bot": "rooster:bot",
                },
            },
        }
    )
    return config


def test_from_name_and_dict():
    name = "cow"
    value = {
        "bot": "module:attribute",
    }

    cow = CowConfig.from_name_and_dict(name, value)

    assert cow.name == name
    assert cow.module == "module"
    assert cow.attribute == "attribute"


def test_load_config(test_config):
    herd = HerdConfig.from_settings(test_config)

    assert len(herd.cows) == 2

    moocow = herd.for_name("moocow")

    assert moocow.name == "moocow"


def test_load_from_cow_config():
    name = "cow"
    value = {
        "bot": "roboherd.examples.moocow:moocow",
    }

    cow = CowConfig.from_name_and_dict(name, value)

    assert isinstance(cow.load(), RoboCow)


def test_names(test_config):
    herd = HerdConfig.from_settings(test_config)

    assert herd.names == {"moocow", "rooster"}

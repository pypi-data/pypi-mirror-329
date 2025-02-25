import pytest

from roboherd.cow import RoboCow

from .util import import_cow


def test_import_cow():
    cow = import_cow("roboherd.examples.moocow:moocow")

    assert isinstance(cow, RoboCow)
    assert cow.information.handle == "moocow"


def test_import_cow_failed():
    with pytest.raises(ImportError):
        import_cow("robocow:nocow")


def test_import_cow_with_handle():
    cow = import_cow("roboherd.examples.moocow:moocow?handle=horse")

    assert isinstance(cow, RoboCow)
    assert cow.information.handle == "horse"

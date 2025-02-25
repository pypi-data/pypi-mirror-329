from fast_depends import Depends
from typing import Annotated

from roboherd.cow import RoboCow


def get_profile(cow: RoboCow) -> dict:
    return cow.profile


Profile = Annotated[dict, Depends(get_profile)]
"""The profile of the cow"""

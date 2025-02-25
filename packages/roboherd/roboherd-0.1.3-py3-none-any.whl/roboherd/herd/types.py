from typing import Callable
from dataclasses import dataclass

from roboherd.cow import RoboCow


@dataclass
class HandlerInformation:
    action: str
    activity_type: str
    func: Callable
    cow: RoboCow

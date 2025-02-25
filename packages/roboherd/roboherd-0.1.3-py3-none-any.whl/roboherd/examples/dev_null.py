from roboherd.cow import RoboCow
from roboherd.cow.types import Information

from .meta import meta_information

bot = RoboCow(
    information=Information(
        name="/dev/null",
        description="""I don't do anything.""",
        handle="devnull",
        meta_information=meta_information,
    )
)

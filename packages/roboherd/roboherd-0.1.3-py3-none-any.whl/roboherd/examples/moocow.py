import logging

from roboherd.cow import RoboCow
from roboherd.annotations import EmbeddedObject, PublishObject
from roboherd.cow.types import Information
from .meta import meta_information

logger = logging.getLogger(__name__)

moocow = RoboCow(
    information=Information(
        handle="moocow",
        name="The mooing cow 🐮",
        description="""I'm a cow that likes to moo.

I also serve as an example for the RoboHerd python tool.
See <a href="https://codeberg.org/helge/roboherd">codeberg.org</a>.""",
        meta_information=meta_information,
    )
)


@moocow.incoming_create
async def on_incoming_create(obj: EmbeddedObject, publisher: PublishObject):
    recipient = obj.get("attributedTo")

    logger.info("Replying to %s", recipient)

    obj = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Note",
        "attributedTo": moocow.actor_id,
        "to": [recipient],
        "cc": ["https://www.w3.org/ns/activitystreams#Public"],
        "content": "moo",
        "inReplyTo": obj.get("id"),
    }

    await publisher(obj)

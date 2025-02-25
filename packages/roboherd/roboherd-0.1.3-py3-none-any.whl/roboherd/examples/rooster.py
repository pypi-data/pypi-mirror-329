from roboherd.cow import RoboCow
from roboherd.cow.types import Information

from roboherd.annotations import PublishObject
from roboherd.annotations.bovine import ObjectFactory

from .meta import meta_information

bot = RoboCow(
    information=Information(
        handle="rooster",
        name="The crowing rooster 🐓",
        meta_information=meta_information,
    )
)


@bot.cron("42 * * * *")
async def crow(publisher: PublishObject, object_factory: ObjectFactory):
    await publisher(
        object_factory.note(content="cock-a-doodle-doo").as_public().build()
    )

import random
from urllib.parse import urlparse

from almabtrieb import Almabtrieb

from roboherd.cow import RoboCow
from roboherd.annotations import PublishObject
from roboherd.annotations.bovine import ObjectFactory
from roboherd.cow.types import Information
from .meta import meta_information


def hostname(actor_id):
    return urlparse(actor_id).netloc


bot = RoboCow(
    information=Information(
        handle="even",
        description="""<p>I'm a bot by Helge. I post a random number every hour. When posting an even number, I change my Fediverse handle to even. When posting an odd one, I use odd.</p>

<p>I also update my name. I'm not sure how you should display my handle with your Fediverse application. Please write a FEP explaining it.</p>""",
        meta_information=meta_information,
    )
)


@bot.startup
async def startup(connection: Almabtrieb, actor_id: str):
    await connection.trigger(
        "update_actor",
        {
            "actor": actor_id,
            "actions": [
                {
                    "action": "add_identifier",
                    "identifier": f"acct:odd@{hostname(actor_id)}",
                    "primary": False,
                }
            ],
        },
    )


@bot.cron("* * * * *")
async def post_number(
    connection: Almabtrieb,
    publisher: PublishObject,
    factory: ObjectFactory,
    actor_id: str,
):
    number = random.randint(0, 1000)

    note = factory.note(content=f"Number: {number}").as_public().build()
    await publisher(note)

    handle = "even" if number % 2 == 0 else "odd"

    await connection.trigger(
        "update_actor",
        {
            "actor": actor_id,
            "actions": [
                {
                    "action": "update_identifier",
                    "identifier": f"acct:{handle}@{hostname(actor_id)}",
                    "primary": True,
                }
            ],
            "profile": {"name": f"Posted an {handle} number"},
        },
    )

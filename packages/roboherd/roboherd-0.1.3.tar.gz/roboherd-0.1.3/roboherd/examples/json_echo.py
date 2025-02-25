import json

from roboherd.cow import RoboCow
from roboherd.annotations import RawData, PublishObject
from roboherd.annotations.bovine import ObjectFactory

from roboherd.cow.types import Information
from .meta import meta_information

bot = RoboCow(
    information=Information(
        handle="jsonecho",
        name="JSON Echo {}",
        description="""<p>I'm a silly bot that replies to
you with the JSON as received through a HTTP
post request by 
<a href="https://codeberg.org/helge/cattle_grid">cattle_grid</a>.</p>
    
    """,
        meta_information=meta_information,
    )
)


def reply_content(raw: dict) -> str:
    """Formats and escapes the JSON data:

    ```pycon
    >>> reply_content({"html": "<b>bold</b>"})
    '<pre><code>{\\n  "html": "&lt;b&gt;bold&lt;/b&gt;"\\n}</code></re>'

    ```
    """
    json_formatted = (
        json.dumps(raw, indent=2)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"<pre><code>{json_formatted}</code></re>"


@bot.incoming_create
async def create(
    raw: RawData, publish_object: PublishObject, object_factory: ObjectFactory
):
    note = (
        object_factory.reply(
            raw.get("object"),
            content=reply_content(raw),
        )
        .as_public()
        .build()
    )

    await publish_object(note)

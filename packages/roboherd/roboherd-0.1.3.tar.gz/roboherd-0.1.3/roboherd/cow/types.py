from pydantic import BaseModel, Field


class MetaInformation(BaseModel):
    """Meta Information about the bot. This includes
    information such as the author and the source repository"""

    source: str | None = Field(
        None,
        examples=["https://forge.example/repo"],
        description="The source repository",
    )

    author: str | None = Field(
        None,
        examples=["acct:author@domain.example"],
        description="The author, often a Fediverse handle",
    )


class Information(BaseModel):
    """Information about the cow"""

    type: str = Field(
        "Service", examples=["Service"], description="ActivityPub type of the actor."
    )

    handle: str | None = Field(
        None,
        examples=["moocow"],
        description="Used as the handle in `acct:handle@domain.example`",
    )

    name: str | None = Field(
        None,
        examples=["The mooing cow 🐮"],
        description="The display name of the cow",
    )

    description: str | None = Field(
        None,
        examples=[
            "I'm a cow that moos.",
            """<p>An example bot to illustrate Roboherd</p><p>For more information on RoboHerd, see <a href="https://codeberg.org/bovine/roboherd">its repository</a>.</p>""",
        ],
        description="The description of the cow, used as summary of the actor",
    )

    frequency: str | None = Field(
        None,
        examples=["daily"],
        description="Frequency of posting. Is set automatically if cron expressions are used.",
    )

    meta_information: MetaInformation = Field(
        MetaInformation(),
        description="Meta information about the cow, such as the source repository",
    )

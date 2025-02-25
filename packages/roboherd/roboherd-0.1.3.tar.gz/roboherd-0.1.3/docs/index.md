# Roboherd

Roboherd is a tool to build automated Fediverse actors. It does
so by connecting to a server through the [Cattle Drive protocol](https://bovine.codeberg.page/cattle_grid/cattle_drive/) protocol. Once you have
configured the connection, all other tasks can be done using
python code and a toml configuration file.

## Tour of the functionality

We will now tour how to write bots with Roboherd. We start with
a basic bot that does nothing except have a profile. Then we will
start by adding features.

### Basic bot aka how to configure the profile

The configuration file defines the actor by a name and the used python file,
e.g.

```toml title="roboherd.toml"
base_url = "https://dev.bovine.social"

[cow.devnull]
bot = "roboherd.examples.dev_null:bot"
```

Where the module is defined as

```python title="roboherd/examples/dev_null.py"
--8<-- "roboherd/examples/dev_null.py"
```

One should note that the above definition describes the properties of
the actor. In mastodon this looks like

??? info "Mastodon Screenshot"
    ![Screen shot of @devnull@dev.bovine.social on mastodon.social](assets/mastodon.png)

??? info "Actor Profile as json"
    ```json
    {
        "attachment": [
            {
            "type": "PropertyValue",
            "name": "Author",
            "value": "acct:helge@mymath.rocks"
            },
            {
            "type": "PropertyValue",
            "name": "Source",
            "value": "https://codeberg.org/bovine/roboherd"
            }
        ],
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
            {
            "PropertyValue": {
                "@id": "https://schema.org/PropertyValue",
                "@context": {
                "value": "https://schema.org/value",
                "name": "https://schema.org/name"
                }
            }
            }
        ],
        "publicKey": {
            "id": "https://dev.bovine.social/actor/5Dhr1Bk_E_WuNik_ii0BBQ#legacy-key-1",
            "owner": "https://dev.bovine.social/actor/5Dhr1Bk_E_WuNik_ii0BBQ",
            "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvUWtZLOftKTRpNJ+t6Bq\nma6hyRKwcbl6LVuZl+dJ+lAfKpEPRx/2uo/1LkA4mUVEVewyhWMQ8SyIoRayuDqP\njDUaai4mohSg+ReNvmWXD4mgGB7XPc00A4Yk2R/u2hkmu8hWLU7260BTQwmpjsyK\nDG7QWvZYbob1Hyr1QabOpn4tUS3pOl6KqGw8ijNUtAYw22kZl/aZ0v/mk7+V2xhT\nsZbRAC/7o39sFvgGdRHsDwXbJX63aU+qpBc7UX42fdOH9pfmRl5Ps7xCfB1iSlQP\nR4BTGbJB9DOLYlvb2iTqh5cn37VYBxNG3haAv34Q3fBPONOe77CeV1abKTr8/jCG\nsQIDAQAB\n-----END PUBLIC KEY-----\n"
        },
        "id": "https://dev.bovine.social/actor/5Dhr1Bk_E_WuNik_ii0BBQ",
        "type": "Service",
        "inbox": "https://dev.bovine.social/inbox/nAy02r0LlQJ0WO5ry2-LFA",
        "outbox": "https://dev.bovine.social/outbox/7JZSBh-1ZXgTXzkSDjGr-A",
        "followers": "https://dev.bovine.social/followers/90-KDZpuvSif5KAL_TzoYQ",
        "following": "https://dev.bovine.social/following/jrp61fFlLDA5HcYDN98JRA",
        "preferredUsername": "devnull",
        "name": "/dev/null",
        "summary": "I don't do anything.",
        "identifiers": [
            "acct:devnull@dev.bovine.social",
            "https://dev.bovine.social/actor/5Dhr1Bk_E_WuNik_ii0BBQ"
        ],
        "endpoints": {
            "sharedInbox": "https://dev.bovine.social/shared_inbox"
        }
    }
    ```

Setting me as the author and the source code is contained in [meta_information][roboherd.cow.types.MetaInformation].

```python title="roboherd/examples/meta.py"
--8<-- "roboherd/examples/meta.py"
```

!!! todo
    How to configure a profile picture [roboherd#10](https://codeberg.org/bovine/roboherd/issues/10)

### Posting on startup

By adding

```python
@bot.startup
async def startup(publish_object: PublishObject, object_factory: ObjectFactory):
    await publish_object(object_factory.note(content="Booo! 🐦").as_public().build())
```

one can post on startup. Here  [PublishObject][roboherd.annotations.PublishObject]
and [ObjectFactory][roboherd.annotations.bovine.ObjectFactory]
are annotations that are injected
through [FastDepends](https://lancetnik.github.io/FastDepends/).

PublishObject depends on the [simple storage extension of cattle_grid](https://bovine.codeberg.page/cattle_grid/extensions/simple_storage/), whereas
ObjectFactory injects an [ObjectFactory][bovine.activitystreams.object_factory.ObjectFactory] provided by the [bovine](https://bovine.readthedocs.io/en/latest/) library.

???info "Full source"
    ```python title="roboherd/examples/scarecrow.py"
    --8<-- "roboherd/examples/scarecrow.py"
    ```

### Replying to messages

By adding a block such as

```python
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
```

one can reply to messages. Here [RawData][roboherd.annotations.RawData] is an annotation that will ensure that the received activity is injected
through [FastDepends](https://lancetnik.github.io/FastDepends/).
The same is true for [PublishObject][roboherd.annotations.PublishObject]
and [ObjectFactory][roboherd.annotations.bovine.ObjectFactory]. The last
one depends on [bovine](https://bovine.readthedocs.io/en/latest/).

`@bot.incoming_create` indicates that the coroutine `create` should be
called when a `Create` activity is received. See [roboherd.cow.RoboCow.incoming_create][].

???info "Full source"
    ```python title="roboherd/examples/json_echo.py"
    --8<-- "roboherd/examples/json_echo.py"
    ```

### Scheduling a message

By including

```python
@bot.cron("42 * * * *")
async def crow(publisher: PublishObject, object_factory: ObjectFactory):
    await publisher(
        object_factory.note(content="cock-a-doodle-doo").as_public().build()
    )
```

one can schedule a message to be published at the 42nd minute of every hour.
Here `"42 * * * *"` is a cron expression.

???info "Full source"
    ```python title="roboherd/examples/rooster.py"
    --8<-- "roboherd/examples/rooster.py"
    ```

!!!tip
    Alternatively one can write [bots that post on startup](#posting-on-startup) and schedule them using cron.

## Installation

### Using the docker container

By running

```bash
docker run --rm -ti -v .:/app helgekr/roboherd
```

you can run a docker container mounting the current directory.
If the current directory contains a `roboherd.toml` file
and the appropriate bots, one can run these bots
by running

```bash
roboherd run
```

inside the container. Alternatively, this can be done directly
by running

```bash
docker run --rm -v .:/app helgekr/roboherd roboherd run
```

### Installing roboherd as a python package

To install roboherd with [bovine](https://bovine.readthedocs.io/en/latest/) support run

```bash
pip install roboherd[bovine]
```

You are then able to run the roboherd command either by

```bash
roboherd run
```

or

```bash
python -mroboherd run
```

## Configuration

roboherd has three global configuration variables, e.g.

```toml title="roboherd.toml"
connection_string = "wss://NAME:PASSWORD@host.example/ws"
base_url = "https://host.example"
echo = false
```

`connection_string` points to the server providing a Cattle Drive endpoint. This connection string currently contains the authentication data.

`base_url` specifies the domain being used to create the bots. With the above configuration file, it would lead to bots with Fediverse handle `acct:BOT-NAME@host.example`. This might be relaxed in the future with
[roboherd#12](https://codeberg.org/bovine/roboherd/issues/12).

Setting `echo` to `true` will  cause roboherd to print all messages performed through Cattle Drive to the console.

### Overriding the configuration through environment variables

Roboherd uses environment variables starting with `ROBOHERD_`
as overrides for the configuration. This is done
through [DynaConf](https://www.dynaconf.com/envvars/). So
for example

```bash
ROBOHERD_CONNECTION_STRING=wss://NAME:PASSWORD@other.example/ws\
    roboherd run
```

will connect to `other.example` instead of `host.example`.

### Using dev.bovine.social

In order to encourage experimentation, I host an _instance_ at
[dev.bovine.social](https://dev.bovine.social/), where
you can quickly sign up and deploy some bots.

Getting start is simple, run

```bash
docker run --rm -v .:/app helgekr/roboherd\
    roboherd register --name NAME --fediverse acct:your@handle.example
```

you will then be prompted for a password.
Afterwards a `roboherd.toml` file with the appropriate configuration
will be created. Now, you can write a bot, add it to `roboherd.toml`
and run it via

```bash
docker run --rm -v .:/app helgekr/roboherd roboherd run
```

Please be respectful to the rest of the Fediverse when using
this service.

### console.bovine.social

After signing up, you can open the
[cattle_grid console](https://console.bovine.social/)
and use it to explore your bots. First one has to sign in
at the top right corner. Afterwards, one should be able
to see the incoming and outgoing messages by selecting
the appropriate points in the menu on the left.

!!! warning
    This still seems somewhat buggy, see
    [cattle_grid#83](https://codeberg.org/bovine/cattle_grid/issues/83)

The console also allows you to lookup Fediverse
objects as seen through cattle_grid and perform actions
manually.

## Developing roboherd

Roboherd uses [astral-uv](https://docs.astral.sh/uv/) and
[hatch](https://hatch.pypa.io/latest/) for development. After
cloning the repository, run

```bash
uv sync --all-extras
```

to install dependencies using uv. Then one can run tests via

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

### Releasing

Releases, packages, documentation, and docker containers are
build automatically using the CI. For this increase the
version, have a [milestone](https://codeberg.org/bovine/roboherd/milestones)
matching the new version, and appropriate entries in
`CHANGES.md`. Then once a pull request with this is merged,
the rest happens automatically.

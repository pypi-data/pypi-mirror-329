import click
import logging
import copy
import importlib
from importlib import import_module
from urllib.parse import parse_qs, urlparse

from almabtrieb import Almabtrieb

from roboherd.cow import RoboCow

logger = logging.getLogger(__name__)


def parse_connection_string(connection_string: str) -> dict:
    """
    Parse a connection string into a dictionary of connection parameters.

    ```pycon
    >>> parse_connection_string("ws://user:pass@host/ws")
    {'host': 'host',
        'port': 80,
        'username': 'user',
        'password': 'pass',
        'websocket_path': '/ws'}

    >>> parse_connection_string("wss://user:pass@host/ws")
    {'host': 'host',
        'port': 443,
        'username': 'user',
        'password': 'pass',
        'websocket_path': '/ws'}

    ```
    """

    parsed = urlparse(connection_string)

    default_port = 80 if parsed.scheme == "ws" else 443

    return {
        "host": parsed.hostname,
        "port": parsed.port or default_port,
        "username": parsed.username,
        "password": parsed.password,
        "websocket_path": parsed.path,
    }


def load_cow(module_name: str, attribute: str) -> RoboCow:
    """Loads a cow from module name and attribute"""
    module = import_module(module_name)
    importlib.reload(module)

    cow = getattr(module, attribute)

    return copy.deepcopy(cow)


def import_cow(name: str) -> RoboCow:
    """Imports a cow from a string of the form
    `module.name:attribute`. Here attribute should
    be of type [roboherd.cow.RoboCow][roboherd.cow.RoboCow].

    ```pycon
    >>> cow = import_cow("roboherd.examples.moocow:moocow")
    >>> cow.information.handle
    'moocow'

    ```
    """
    try:
        query = None
        module_name, attribute = name.split(":")
        if "?" in attribute:
            attribute, query = attribute.split("?")

        cow = load_cow(module_name, attribute)

        if query:
            parsed_query = parse_qs(query)
            handle = parsed_query.get("handle", [None])[0]
            if handle:
                cow.information.handle = handle

        return cow

    except Exception as e:
        logger.error("Failed to import cow with name: %s", name)
        logger.error("names should have the form module:attribute")
        logger.exception(e)

        raise ImportError("Failed to load module")


def create_connection(ctx):
    connection_string = ctx.obj["connection_string"]
    base_url = ctx.obj["base_url"]

    if not connection_string:
        click.echo("ERROR: No connection string provided")
        click.echo(
            "either provide one through --connection_string or set it in your configuration file"
        )
        exit(1)

    if not base_url:
        click.echo("ERROR: No base url for cows provided")
        click.echo(
            "either provide one through --base_url or set it in your configuration file"
        )
        exit(1)

    ctx.obj["connection"] = Almabtrieb.from_connection_string(
        connection_string, echo=ctx.obj["settings"].get("echo", False)
    )

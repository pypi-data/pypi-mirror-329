import asyncio
import logging
import os

import click
import dynaconf
import watchfiles

from roboherd.herd import RoboHerd
from roboherd.herd.manager import HerdManager
from roboherd.util import create_connection
from roboherd.register import register as run_register

logging.basicConfig(level=logging.INFO)


@click.group()
@click.option(
    "--connection_string",
    default=None,
    help="Connection string to the websocket mqtt broker",
)
@click.option(
    "--base_url",
    default=None,
    help="Base url to create cows with",
)
@click.option("--config_file", default="roboherd.toml", help="Configuration file")
@click.pass_context
def main(ctx, connection_string, base_url, config_file):
    """Configuration is usually loaded from the config_file. These options can be overwritten by passing as a command line argument."""
    settings = dynaconf.Dynaconf(
        settings_files=[config_file],
        envvar_prefix="ROBOHERD",
    )
    ctx.ensure_object(dict)

    ctx.obj["config_file"] = config_file
    ctx.obj["settings"] = settings

    if connection_string:
        ctx.obj["connection_string"] = connection_string
    else:
        ctx.obj["connection_string"] = settings.get("connection_string")

    if base_url:
        ctx.obj["base_url"] = base_url
    else:
        ctx.obj["base_url"] = settings.get("base_url")


@main.command()
@click.pass_context
def run(ctx):
    """Runs the roboherd by connecting to the server."""

    create_connection(ctx)

    herd = RoboHerd(base_url=ctx.obj["base_url"])

    settings = ctx.obj["settings"]

    if settings.get("cow"):
        herd.manager = HerdManager.from_settings(settings)
        asyncio.run(herd.run(ctx.obj["connection"]))
    else:
        click.echo("No cows specified")
        exit(1)


@main.command()
@click.pass_context
def watch(ctx):
    """Watches the file the module is in for changes and then restarts roboherd.

    Note: Options for roboherd are currently ignored (FIXME)."""

    watchfiles.run_process("roboherd", target="roboherd run")


@main.command()
@click.pass_context
@click.option("--name", help="Name for the account to be created", prompt=True)
@click.option(
    "--password",
    help="Password for the account to be created",
    hide_input=True,
    prompt=True,
)
@click.option("--fediverse", help="Fediverse handle", prompt=True)
def register(ctx, name, password, fediverse):
    """Registers a new account on dev.bovine.social. All three options are required. If not provided, you will be prompted for them."""

    if os.path.exists(ctx.obj["config_file"]):
        click.echo("Config file already exists")
        exit(1)

    if len(password) < 6:
        click.echo("Password should have at least 6 characters")
        exit(1)

    asyncio.run(run_register(ctx.obj["config_file"], name, password, fediverse))


if __name__ == "__main__":
    main()

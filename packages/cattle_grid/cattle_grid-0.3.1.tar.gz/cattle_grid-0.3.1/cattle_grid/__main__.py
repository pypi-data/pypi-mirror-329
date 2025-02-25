import click
import os
import asyncio
import logging

from cattle_grid.config import load_settings, default_filenames
from .statistics import statistics
from .auth.block_cli import add_block_command
from .auth.key_cli import add_keys_command
from .actors import add_actors_to_cli_as_group
from .extensions.cli import add_extension_commands_as_group
from .account.cli import add_account_commands

logger = logging.getLogger(__name__)


@click.group()
@click.option("--config_file", default="cattle_grid.toml")
@click.pass_context
def main(ctx, config_file):
    ctx.ensure_object(dict)
    ctx.obj["config_file"] = config_file

    try:
        ctx.obj["config"] = load_settings(config_file)
    except Exception as e:
        logger.Exception(e)


@main.command()
@click.option(
    "--force",
    help="Used to override the old configuration file",
    is_flag=True,
    default=False,
)
@click.pass_context
def new_config(ctx, force):
    """Creates a new configuration file"""
    filename = ctx.obj["config_file"]

    if os.path.exists(filename) and not force:
        print("Configuration file already exists! Use --force to overwrite.")
        exit(1)

    # FIXME

    exit(1)


@main.command()
@click.pass_context
def stat(ctx):
    """Displays statistical information about cattle_grid"""
    asyncio.run(statistics(ctx.obj["config"]))


@main.command()
@click.option("--db_uri")
@click.option("--name")
@click.pass_context
def create_db_migration(ctx, db_uri, name):
    """Creates a database migration; run after editing models"""
    from .database import migrate

    config = ctx.obj["config"]

    if db_uri:
        config.db_uri = db_uri

    asyncio.run(migrate(config, name))


@main.command()
@click.option("--db_uri")
@click.pass_context
def upgrade_db(ctx, db_uri):
    from .database import upgrade

    config = ctx.obj["config"]

    if db_uri:
        config.db_uri = db_uri

    asyncio.run(upgrade(config))


@main.command()
@click.option("--filename", default="asyncapi.json")
@click.option(
    "--component",
    default=None,
    help="Restrict to a component. Currently allowed ap",
)
def async_api(filename, component):
    if component == "ap":
        from .activity_pub import get_async_api_schema
    elif component == "account":
        from .account.router.schema import get_async_api_schema
    else:
        from .exchange import get_async_api_schema

    schema = get_async_api_schema().to_json()

    with open(filename, "w") as fp:
        fp.write(schema)


@main.command()
@click.option("--filename", default="openapi.json")
@click.option(
    "--component",
    default=None,
    help="Restrict to a component. Currently allowed auth or ap",
)
@click.pass_context
def openapi(ctx, filename, component):
    import json

    match component:
        case "auth":
            from .auth import create_app

            app = create_app(default_filenames)
        case "ap":
            from .activity_pub import get_fastapi_app

            app = get_fastapi_app()
        case "account":
            from .account.server.app import app
        case "rabbit":
            from .account.rabbit import app_for_schema

            app = app_for_schema()
        case _:
            from . import create_app

            # app = create_app(ctx.obj["config_file"])
            app = create_app()
    with open(filename, "w") as fp:
        json.dump(app.openapi(), fp)


add_block_command(main)
add_keys_command(main)
add_extension_commands_as_group(main)
add_account_commands(main)
add_actors_to_cli_as_group(main)

if __name__ == "__main__":
    main()

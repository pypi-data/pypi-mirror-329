import asyncio
import click

from cattle_grid.database import database

from .model import RemoteIdentity


async def prune_keys(config):
    try:
        async with database(config.db_uri):
            await RemoteIdentity.filter().delete()
    except Exception:
        print("Failed to purge remote identifiers")


def add_keys_command(main):
    @main.group()
    @click.pass_context
    def keys(ctx):
        """Allows the management of public keys"""
        if "config" not in ctx.obj:
            print("Could not load config and it is necessary for keys management")
            exit(1)

    @keys.command()
    @click.option(
        "--all_flag", help="Remove all known public keys", default=False, is_flag=True
    )
    @click.pass_context
    def clear(ctx, all_flag):
        try:
            asyncio.run(prune_keys(ctx.obj["config"]))
        except Exception as e:
            print(e)

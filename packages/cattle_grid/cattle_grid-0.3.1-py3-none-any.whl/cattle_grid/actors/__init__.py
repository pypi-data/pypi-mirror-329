import asyncio

import click

from cattle_grid.activity_pub.models import Actor, ActorStatus
from cattle_grid.account.models import (
    ActorForAccount,
    ActorStatus as ActorStatusForAccount,
)
from cattle_grid.database import run_with_database


async def list_actors(deleted: bool = False):
    result = await Actor.filter().all()

    if deleted:
        result = [x for x in result if x.status == ActorStatus.deleted]

    for x in result:
        print(x.actor_id)

    if len(result) == 0:
        print("No actors")


async def prune_actors():
    await Actor.filter(status=ActorStatus.deleted).delete()
    await ActorForAccount.filter(status=ActorStatusForAccount.deleted).delete()


def add_actors_to_cli_as_group(main):
    @main.group()
    def actor():
        """Used to manage actors"""

    add_to_cli(actor)


def add_to_cli(main):
    @main.command("list")  # type: ignore
    @click.option(
        "--deleted", is_flag=True, default=False, help="Only list deleted actors"
    )
    @click.pass_context
    def list_actors_command(ctx, deleted):
        asyncio.run(run_with_database(ctx.obj["config"], list_actors(deleted)))

    @main.command("prune")  # type: ignore
    @click.pass_context
    def prune_actors_command(ctx):
        asyncio.run(run_with_database(ctx.obj["config"], prune_actors()))

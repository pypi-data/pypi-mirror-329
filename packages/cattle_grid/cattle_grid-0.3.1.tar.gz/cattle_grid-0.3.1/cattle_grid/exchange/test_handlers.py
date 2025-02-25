from unittest.mock import AsyncMock

from cattle_grid.testing.fixtures import *  # noqa
from cattle_grid.testing import mocked_config

from cattle_grid.activity_pub.actor import actor_to_object
from cattle_grid.activity_pub.models import PublicIdentifier

from cattle_grid.model.exchange import (
    UpdateActorMessage,
    UpdateIdentifierAction,
    UpdateActionType,
)
from .handlers import update_actor


async def test_update_actor_unknown_actor():
    msg = UpdateActorMessage(actor="no_id", profile={})

    await update_actor(msg)


async def test_update_actor(test_actor):
    new_name = "Alyssa Newton"
    msg = UpdateActorMessage(actor=test_actor.actor_id, profile={"name": new_name})

    await update_actor(msg, AsyncMock())

    await test_actor.refresh_from_db()

    obj = actor_to_object(test_actor)

    assert obj.get("name") == new_name


async def test_update_actor_profile_not_overwritten(test_actor):
    new_name = "Alyssa Newton"
    new_description = "I was originally called Leibnitz. Also I'm a cat."
    msg = UpdateActorMessage(actor=test_actor.actor_id, profile={"name": new_name})

    await update_actor(msg, AsyncMock())
    await test_actor.refresh_from_db()

    obj = actor_to_object(test_actor)
    assert obj.get("name") == new_name

    msg = UpdateActorMessage(
        actor=test_actor.actor_id, profile={"summary": new_description}
    )

    await update_actor(msg, AsyncMock())
    await test_actor.refresh_from_db()

    obj = actor_to_object(test_actor)
    assert obj.get("name") == new_name


async def test_create_identifier(test_actor_with_account):
    with mocked_config({"frontend": {"base_urls": ["http://localhost"]}}):
        identifier = "acct:new@localhost"
        new_identifier = UpdateIdentifierAction(
            action=UpdateActionType.create_identifier,
            identifier=identifier,
            primary=False,
        )

        msg = UpdateActorMessage(
            actor=test_actor_with_account.actor_id, actions=[new_identifier]
        )

        await update_actor(msg, AsyncMock())

        await test_actor_with_account.refresh_from_db()
        await test_actor_with_account.fetch_related("identifiers")

        obj = actor_to_object(test_actor_with_account)

        assert identifier in obj.get("identifiers", [])


async def test_update_identifier(test_actor):
    identifier = "acct:one@localhost"
    await PublicIdentifier.create(
        actor=test_actor,
        identifier="acct:two@localhost",
        name="through_exchange",
        preference=1,
    )
    await PublicIdentifier.create(
        actor=test_actor,
        identifier=identifier,
        name="through_exchange",
        preference=0,
    )

    await test_actor.refresh_from_db()
    await test_actor.fetch_related("identifiers")

    obj = actor_to_object(test_actor)

    assert obj["preferredUsername"] == "two"

    update_identifier = UpdateIdentifierAction(
        action=UpdateActionType.update_identifier,
        identifier=identifier,
        primary=True,
    )

    msg = UpdateActorMessage(actor=test_actor.actor_id, actions=[update_identifier])

    await update_actor(msg, AsyncMock())

    await test_actor.refresh_from_db()
    await test_actor.fetch_related("identifiers")

    obj = actor_to_object(test_actor)

    assert obj["preferredUsername"] == "one"

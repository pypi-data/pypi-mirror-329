import pytest

from cattle_grid.testing.fixtures import *  # noqa
from cattle_grid.model import ActivityMessage

from cattle_grid.activity_pub.models import Follower, Following

from .util import update_recipients_for_collections


@pytest.fixture
def message(test_actor):  # noqa
    return ActivityMessage(actor=test_actor.actor_id, data={})


async def test_update_recipients_for_collection(message, test_actor):  # noqa
    recipients = {"http://remote.test"}

    result = await update_recipients_for_collections(message, recipients)

    assert result == recipients


async def test_update_recipients_for_collection_with_followers(
    message,
    test_actor,  # noqa
):
    recipients = {"http://remote.test", test_actor.followers_uri}

    await Follower.create(
        actor=test_actor, follower="http://follower.test", accepted=True, request="none"
    )

    result = await update_recipients_for_collections(message, recipients)

    assert result == {"http://remote.test", "http://follower.test"}


async def test_update_recipients_for_collection_for_following_followers(
    message,
    test_actor,  # noqa
):
    recipients = {
        "http://remote.test",
        test_actor.followers_uri,
        test_actor.following_uri,
    }

    await Follower.create(
        actor=test_actor, follower="http://follower.test", accepted=True, request="none"
    )
    await Following.create(
        actor=test_actor,
        following="http://following.test",
        accepted=True,
        request="none",
    )

    result = await update_recipients_for_collections(message, recipients)

    assert result == {"http://remote.test", "http://follower.test"}


async def test_update_recipients_for_collection_for_self_delete(
    message,
    test_actor,  # noqa
):
    recipients = {
        "http://remote.test",
        test_actor.followers_uri,
        test_actor.following_uri,
    }

    await Follower.create(
        actor=test_actor, follower="http://follower.test", accepted=True, request="none"
    )
    await Following.create(
        actor=test_actor,
        following="http://following.test",
        accepted=True,
        request="none",
    )

    message.data = {
        "type": "Delete",
        "actor": test_actor.actor_id,
        "object": test_actor.actor_id,
    }

    result = await update_recipients_for_collections(message, recipients)

    assert result == {
        "http://remote.test",
        "http://follower.test",
        "http://following.test",
    }

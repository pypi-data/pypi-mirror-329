import pytest

from unittest.mock import AsyncMock
from cattle_grid.testing.fixtures import *  # noqa

from cattle_grid.activity_pub.models import Follower, Following
from cattle_grid.model import ActivityMessage

from .incoming import (
    incoming_follow_request,
    incoming_accept_activity,
    incoming_reject_activity,
    incoming_delete_activity,
    incoming_block_activity,
    incoming_undo_activity,
)


@pytest.mark.parametrize(
    "object_creator", [lambda x: x, lambda x: {"type": "Person", "id": x}]
)
async def test_incoming_follow_request_create_follower(
    test_actor,  # noqa
    object_creator,
):
    msg = ActivityMessage(
        actor=test_actor.actor_id,
        data={
            "id": "http://remote.test/id",
            "type": "Follow",
            "actor": "http://remote.test/actor",
            "object": object_creator(test_actor.actor_id),
        },
    )
    mock = AsyncMock()

    await incoming_follow_request(msg, actor=test_actor, broker=mock)

    followers = await Follower.filter().all()

    assert len(followers) == 1

    item = followers[0]
    assert item.follower == "http://remote.test/actor"
    assert not item.accepted

    mock.publish.assert_not_awaited()


async def test_incoming_follow_request_invalid(test_actor):  # noqa
    msg = ActivityMessage(
        actor=test_actor.actor_id,
        data={
            "id": "http://remote.test/id",
            "type": "Follow",
            "actor": "http://remote.test/actor",
        },
    )
    await incoming_follow_request(msg, test_actor, broker=AsyncMock())

    followers = await Follower.filter().all()

    assert len(followers) == 0


async def test_incoming_follow_request_auto_follow(test_actor):  # noqa
    test_actor.automatically_accept_followers = True
    await test_actor.save()

    msg = ActivityMessage(
        actor=test_actor.actor_id,
        data={
            "id": "http://remote.test/id",
            "type": "Follow",
            "actor": "http://remote.test/actor",
            "object": test_actor.actor_id,
        },
    )
    mock = AsyncMock()

    await incoming_follow_request(msg, actor=test_actor, broker=mock)

    mock.publish.assert_awaited_once()


async def test_incoming_accept_activity(test_actor):  # noqa
    follow_id = "follow:1234"
    remote = "http://remote.test/actor"

    following = await Following.create(
        actor=test_actor, following=remote, request=follow_id, accepted=False
    )

    msg = ActivityMessage(
        actor=test_actor.actor_id,
        data={
            "id": "http://remote.test/id",
            "type": "Accept",
            "actor": remote,
            "object": follow_id,
        },
    )
    await incoming_accept_activity(msg, test_actor, broker=AsyncMock())

    await following.refresh_from_db()

    assert following.accepted


async def test_incoming_accept_not_found(test_actor):  # noqa
    remote = "http://remote.test/actor"

    msg = ActivityMessage(
        actor=test_actor.actor_id,
        data={
            "id": "http://remote.test/id",
            "type": "Accept",
            "actor": remote,
            "object": "do_not_exist",
        },
    )
    await incoming_accept_activity(msg, test_actor, broker=AsyncMock())


async def test_incoming_reject(test_actor):  # noqa
    broker = AsyncMock()

    await Following.create(
        actor=test_actor,
        following="http://remote.test/",
        accepted=True,
        request="http://actor.test/follow",
    )

    await incoming_reject_activity(
        ActivityMessage(
            actor=test_actor.actor_id,
            data={
                "id": "http://actor.test/follow/reject",
                "type": "Reject",
                "actor": "http://remote.test",
                "object": "http://actor.test/follow",
            },
        ),
        test_actor,
        broker,
    )

    following_count = await Following.filter().count()

    assert following_count == 0


async def test_incoming_delete(test_actor):  # noqa
    await Following.create(
        actor=test_actor,
        following="http://remote.test/",
        accepted=True,
        request="http://actor.test/follow",
    )

    await Follower.create(
        actor=test_actor,
        follower="http://remote.test/",
        accepted=True,
        request="http://actor.test/other",
    )

    await incoming_delete_activity(
        ActivityMessage(
            actor=test_actor.actor_id,
            data={
                "id": "http://actor.test/follow/delete",
                "type": "Delete",
                "actor": "http://remote.test/",
                "object": "http://remote.test/",
            },
        ),
    )

    follower_count = await Follower.filter().count()
    following_count = await Follower.filter().count()

    assert follower_count == 0
    assert following_count == 0


async def test_incoming_block(test_actor):  # noqa
    broker = AsyncMock()

    await Following.create(
        actor=test_actor,
        following="http://remote.test/",
        accepted=True,
        request="http://actor.test/follow",
    )

    await incoming_block_activity(
        ActivityMessage(
            actor=test_actor.actor_id,
            data={
                "id": "http://actor.test/follow/reject",
                "type": "Block",
                "actor": "http://remote.test/",
                "object": test_actor.actor_id,
            },
        ),
        broker=broker,
        actor=test_actor,
    )

    following_count = await Following.filter().count()

    assert following_count == 0


@pytest.mark.parametrize(
    "object_builder",
    [
        lambda x: x,
        lambda x: {"type": "Follow", "id": x, "actor": "http://remote.test/"},
    ],
)
async def test_incoming_undo_follow(test_actor, object_builder):  # noqa
    broker = AsyncMock()
    follow_request_id = "http://actor.test/follow"

    await Follower.create(
        actor=test_actor,
        follower="http://remote.test/",
        accepted=True,
        request=follow_request_id,
    )

    await incoming_undo_activity(
        ActivityMessage(
            actor=test_actor.actor_id,
            data={
                "id": "http://actor.test/follow/undo",
                "type": "Undo",
                "actor": "http://remote.test/",
                "object": object_builder(follow_request_id),
            },
        ),
        broker=broker,
        actor=test_actor,
    )

    follower_count = await Follower.filter().count()

    assert follower_count == 0

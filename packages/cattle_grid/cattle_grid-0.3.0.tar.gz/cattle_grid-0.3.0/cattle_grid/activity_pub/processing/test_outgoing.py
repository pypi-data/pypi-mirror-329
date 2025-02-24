import pytest
from unittest.mock import AsyncMock

from faststream.rabbit import RabbitBroker, TestRabbitBroker, RabbitQueue

from bovine.activitystreams import factories_for_actor_object

from cattle_grid.activity_pub.actor import create_actor, actor_to_object
from cattle_grid.testing.fixtures import *  # noqa
from cattle_grid.activity_pub.models import Follower, Blocking
from cattle_grid.model import ActivityMessage
from cattle_grid.dependencies.globals import global_container


from .outgoing import (
    create_outgoing_router,
    outgoing_message_distribution,
    outgoing_reject_activity,
    outgoing_block_activity,
    outgoing_undo_request,
)


@pytest.fixture
async def mock_subscriber():
    return AsyncMock()


@pytest.fixture
async def broker(mock_subscriber):
    br = RabbitBroker("amqp://guest:guest@localhost:5672/")
    br.include_router(create_outgoing_router())

    br.subscriber(
        RabbitQueue("test_queue", routing_key="to_send"),
        exchange=global_container.internal_exchange,
    )(mock_subscriber)

    async with TestRabbitBroker(br, connect_only=False) as tbr:
        yield tbr


@pytest.fixture
async def test_actor():
    return await create_actor("http://localhost")


async def test_outgoing_message_no_call(broker, mock_subscriber):
    try:
        await broker.publish(
            {},
            routing_key="outgoing.Activity",
            exchange=global_container.internal_exchange,
        )
    except Exception as e:
        print(e)

    mock_subscriber.assert_not_called()


async def test_outgoing_message(broker, mock_subscriber, test_actor):
    await broker.publish(
        {
            "actor": test_actor.actor_id,
            "data": {"to": "http://remote"},
        },
        routing_key="outgoing.Activity",
        exchange=global_container.internal_exchange,
    )

    mock_subscriber.assert_awaited_once()


async def test_outgoing_message_follower(broker, mock_subscriber, test_actor):
    follower_id = "http://follower.test"
    await Follower.create(
        actor=test_actor, follower=follower_id, request="xxx", accepted=True
    )

    await broker.publish(
        {
            "actor": test_actor.actor_id,
            "data": {"to": test_actor.followers_uri},
        },
        routing_key="outgoing.Activity",
        exchange=global_container.internal_exchange,
    )

    mock_subscriber.assert_awaited_once()
    args = mock_subscriber.call_args

    assert args[1].get("target") == follower_id


async def test_outgoing_follow_request(broker, mock_subscriber, test_actor):
    remote_actor = "http://remote"

    activity_factory, _ = factories_for_actor_object(actor_to_object(test_actor))

    activity = activity_factory.follow(remote_actor, id="follow_id")

    await broker.publish(
        {"actor": test_actor.actor_id, "data": activity},
        routing_key="outgoing.Follow",
        exchange=global_container.internal_exchange,
    )

    await test_actor.fetch_related("following")

    assert 1 == len(test_actor.following)

    assert not test_actor.following[0].accepted
    assert test_actor.following[0].following == remote_actor


async def test_outgoing_accept_request(broker, mock_subscriber, test_actor):
    follow_request_id = "http://remote/id"

    activity_factory, _ = factories_for_actor_object(actor_to_object(test_actor))

    activity = activity_factory.accept(follow_request_id)

    await Follower.create(
        actor=test_actor,
        follower="http://remote",
        request=follow_request_id,
        accepted=False,
    )

    await broker.publish(
        {
            "actor": test_actor.actor_id,
            "data": activity,
        },
        routing_key="outgoing.Accept",
        exchange=global_container.internal_exchange,
    )

    await test_actor.fetch_related("followers")

    assert 1 == len(test_actor.followers)

    assert test_actor.followers[0].accepted


async def test_outgoing_no_message_for_public(test_actor):
    activity_factory, _ = factories_for_actor_object(actor_to_object(test_actor))

    broker = AsyncMock()

    activity = activity_factory.accept("http://remote").as_public().build()

    await outgoing_message_distribution(
        ActivityMessage(
            actor=test_actor.actor_id,
            data=activity,
        ),
        broker,
    )

    broker.publish.assert_not_awaited()


async def test_outgoing_reject(test_actor):
    activity_factory, _ = factories_for_actor_object(actor_to_object(test_actor))

    broker = AsyncMock()

    await Follower.create(
        actor=test_actor,
        follower="http://remote.test/",
        accepted=True,
        request="http://remote.test/follow",
    )

    activity = activity_factory.reject(
        "http://remote.test/follow", to={"http://remote.test/"}
    ).build()

    await outgoing_reject_activity(
        ActivityMessage(
            actor=test_actor.actor_id,
            data=activity,
        ),
        broker,
    )

    follower_count = await Follower.filter().count()

    assert follower_count == 0


async def test_outgoing_block(test_actor):
    activity_factory, _ = factories_for_actor_object(actor_to_object(test_actor))

    broker = AsyncMock()

    await Follower.create(
        actor=test_actor,
        follower="http://remote.test/",
        accepted=True,
        request="http://remote.test/follow",
    )

    activity = activity_factory.block("http://remote.test/").build()

    await outgoing_block_activity(
        ActivityMessage(
            actor=test_actor.actor_id,
            data=activity,
        ),
        actor=test_actor,
        broker=broker,
    )

    follower_count = await Follower.filter().count()

    assert follower_count == 0

    blocking_count = await Blocking.filter().count()
    assert blocking_count == 1


async def test_outgoing_block_then_undo(test_actor):
    activity_factory, _ = factories_for_actor_object(actor_to_object(test_actor))

    broker = AsyncMock()
    block_id = "http://me.test/block_id"

    activity = activity_factory.block("http://remote.test/", id=block_id).build()

    await outgoing_block_activity(
        ActivityMessage(
            actor=test_actor.actor_id,
            data=activity,
        ),
        actor=test_actor,
        broker=broker,
    )

    blocking_count = await Blocking.filter(active=True).count()
    assert blocking_count == 1

    undo = activity_factory.undo(activity).build()

    await outgoing_undo_request(
        ActivityMessage(
            actor=test_actor.actor_id,
            data=undo,
        ),
        actor=test_actor,
        broker=broker,
    )

    blocking_count = await Blocking.filter(active=True).count()
    assert blocking_count == 0

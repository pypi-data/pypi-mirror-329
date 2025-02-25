import logging

from typing import Annotated
from faststream import Depends

from bovine import BovineActor

from cattle_grid.activity_pub.models import Actor
from cattle_grid.model import ActivityMessage, FetchMessage
from cattle_grid.dependencies import ClientSession
from cattle_grid.model.processing import ToSendMessage, StoreActivityMessage

from cattle_grid.activity_pub.actor import (
    bovine_actor_for_actor_id,
)

logger = logging.getLogger(__name__)


class ProcessingError(ValueError): ...


async def actor_id(
    msg: ActivityMessage | FetchMessage | ToSendMessage | StoreActivityMessage,
) -> str:
    return msg.actor


async def actor_for_message(actor_id: str = Depends(actor_id)):
    actor = await Actor.get_or_none(actor_id=actor_id)

    if actor is None:
        raise ProcessingError("Actor not found")

    return actor


async def bovine_actor_for_message(
    actor_id: Annotated[str, Depends(actor_id)],
    session: ClientSession,
) -> BovineActor:
    actor = await bovine_actor_for_actor_id(actor_id)
    if actor is None:
        raise ProcessingError("Actor not found")

    await actor.init(session=session)

    return actor


MessageActor = Annotated[Actor, Depends(actor_for_message)]
MessageBovineActor = Annotated[BovineActor, Depends(bovine_actor_for_message)]

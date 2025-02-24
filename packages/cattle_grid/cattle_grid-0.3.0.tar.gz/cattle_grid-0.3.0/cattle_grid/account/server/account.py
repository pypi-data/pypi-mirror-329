import logging


from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from bovine.types import ServerSentEvent

from cattle_grid.dependencies.fastapi import MethodInformation
from cattle_grid.activity_pub.actor import (
    create_actor,
    actor_to_object,
    DuplicateIdentifierException,
)
from cattle_grid.model.account import InformationResponse, EventType

from cattle_grid.account.models import ActorForAccount
from cattle_grid.account.router.info import create_information_response

from .responses import CreateActorRequest
from .dependencies import CurrentAccount
from .streaming import get_message_streamer

logger = logging.getLogger(__name__)

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.get(
    "/stream/{event_type}",
    response_description="EventSource",
    operation_id="stream",
)
async def stream(
    event_type: EventType,
    account: CurrentAccount,
    request: Request,
    stream_messages=Depends(get_message_streamer),
):
    """EventSource corresponding to all messages received
    by the account.

    This method returns an
    [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
    providing server sent events."""
    username = account.name

    async def event_stream():
        try:
            async for message in stream_messages(username, event_type):
                if await request.is_disconnected():
                    return
                data = ServerSentEvent(data=message).encode()

                yield data
        except Exception as e:
            logger.exception(e)
            raise e

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@account_router.post(
    "/create",
    status_code=201,
    operation_id="create_actor",
    responses={409: {"description": "Duplicate identifier"}},
)
async def create_actor_method(body: CreateActorRequest, account: CurrentAccount):
    """Allows one to create a new actor. The allowed values for base_url
    can be retrieved using the info endpoint."""
    try:
        actor = await create_actor(body.base_url, preferred_username=body.handle)
    except DuplicateIdentifierException:
        raise HTTPException(409, "Duplicate identifier")

    await actor.fetch_related("identifiers")

    name = body.name or "from_api"

    await ActorForAccount.create(account=account, actor=actor.actor_id, name=name)

    return actor_to_object(actor)


@account_router.get("/info", operation_id="account_info")
async def return_account_information(
    account: CurrentAccount, method_information: MethodInformation
) -> InformationResponse:
    """Returns information about the server and the account."""

    if not isinstance(method_information, list):
        logger.warning("Method information is not a list")
        method_information = []

    return await create_information_response(account, method_information)

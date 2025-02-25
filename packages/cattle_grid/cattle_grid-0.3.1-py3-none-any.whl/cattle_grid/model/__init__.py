from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class ActivityMessage(BaseModel):
    """
    Message that contains an Activity. Activity is used as the name for the 'data object' being exchanged, as is common in the Fediverse
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    actor: str
    """
    actor_id of the actor that received the message
    """
    data: Dict[str, Any]
    """
    Activity.
    """


class SharedInboxMessage(BaseModel):
    """
    Message that contains an Activity. In difference to the ActivityMessage this message does not have an actor, and thus its recipients will be determined by cattle_grid.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    data: Dict[str, Any]
    """
    Activity.
    """


class FetchMessage(BaseModel):
    """
    Used to request an ActivityPub object to be retrieved
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    actor: str
    """
    actor_id of the actor that received the message
    """
    uri: str
    """
    URI of the object being retrieved
    """

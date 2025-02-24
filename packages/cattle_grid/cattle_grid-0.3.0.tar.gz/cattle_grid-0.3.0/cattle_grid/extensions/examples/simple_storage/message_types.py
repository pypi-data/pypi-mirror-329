from pydantic import BaseModel, Field


class PublishActivity(BaseModel):
    """Used when publishing an activity"""

    actor: str = Field(examples=["http://alice.example"])
    """The actor performing the activity"""

    data: dict = Field(
        examples=[
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "AnimalSound",
                "actor": "http://alice.example",
                "to": ["http://bob.example"],
                "content": "moo",
            }
        ]
    )
    """Activity to publish"""


class PublishObject(BaseModel):
    """Used when publishing an object"""

    actor: str = Field(examples=["http://alice.example"])
    """The actor performing the activity"""

    data: dict = Field(
        examples=[
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Note",
                "attributedTo": "http://alice.example",
                "to": ["http://bob.example"],
                "content": "moo",
            }
        ]
    )
    """Object to publish"""

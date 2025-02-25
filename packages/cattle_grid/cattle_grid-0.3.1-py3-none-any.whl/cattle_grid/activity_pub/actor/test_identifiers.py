import pytest

from cattle_grid.testing.fixtures import *  # noqa

from cattle_grid.activity_pub.models import PublicIdentifier, PublicIdentifierStatus

from .identifiers import collect_identifiers_for_actor, identifier_in_list_exists


def test_collect_identifiers_for_actor(test_actor):
    identifiers = collect_identifiers_for_actor(test_actor)

    assert identifiers == [test_actor.actor_id]


async def test_collect_identifiers_for_actor_with_acct_uri(test_actor):
    await PublicIdentifier.create(
        actor=test_actor,
        name="webfinger",
        identifier="acct:me@localhost",
        status=PublicIdentifierStatus.verified,
        preference=5,
    )

    await test_actor.fetch_related("identifiers")

    identifiers = collect_identifiers_for_actor(test_actor)

    assert identifiers == ["acct:me@localhost", test_actor.actor_id]


async def test_collect_identifiers_for_actor_with_acct_uri_unverified(test_actor):
    await PublicIdentifier.create(
        actor=test_actor,
        name="webfinger",
        identifier="acct:me@localhost",
        status=PublicIdentifierStatus.unverified,
        preference=5,
    )

    await test_actor.fetch_related("identifiers")

    identifiers = collect_identifiers_for_actor(test_actor)

    assert identifiers == [test_actor.actor_id]


@pytest.mark.parametrize(
    "identifiers, expected",
    [
        ([], False),
        (["acct:one@localhost"], True),
        (["acct:other@localhost"], False),
        (["acct:other@localhost", "acct:one@localhost"], True),
    ],
)
async def test_identifier_in_list_exists(test_actor, identifiers, expected):
    await PublicIdentifier.create(
        actor=test_actor,
        name="webfinger",
        identifier="acct:one@localhost",
        status=PublicIdentifierStatus.unverified,
        preference=5,
    )
    await PublicIdentifier.create(
        actor=test_actor,
        name="webfinger",
        identifier="acct:two@localhost",
        status=PublicIdentifierStatus.unverified,
        preference=5,
    )
    result = await identifier_in_list_exists(identifiers)

    assert result == expected

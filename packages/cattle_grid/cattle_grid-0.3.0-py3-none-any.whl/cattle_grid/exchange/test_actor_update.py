from cattle_grid.testing.fixtures import *  # noqa
from cattle_grid.account.models import ActorForAccount
from cattle_grid.model.exchange import UpdateAction, UpdateActionType

from .actor_update import handle_actor_action


async def test_handle_actor_action_rename(test_actor, test_account):
    actor_for_account = await ActorForAccount.create(
        actor=test_actor.actor_id, account=test_account
    )

    action = UpdateAction(
        action=UpdateActionType.rename,
        name="new name",  # type:ignore
    )

    await handle_actor_action(test_actor, action)

    await actor_for_account.refresh_from_db()

    assert actor_for_account.name == "new name"

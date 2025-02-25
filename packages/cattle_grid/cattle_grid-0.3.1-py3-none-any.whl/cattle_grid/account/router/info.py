from cattle_grid.model.account import (
    NameAndVersion,
    InformationResponse,
    ActorInformation,
)
from cattle_grid.model.extension import MethodInformationModel
from cattle_grid.version import __version__


from cattle_grid.account.models import Account, ActorForAccount, ActorStatus
from cattle_grid.account.permissions import allowed_base_urls


def protocol_and_backend():
    protocol = NameAndVersion(name="CattleDrive", version="0.1.0")
    backend = NameAndVersion(name="cattle_grid", version=__version__)

    return dict(protocol=protocol, backend=backend)


def actor_to_information(actor: ActorForAccount) -> ActorInformation:
    """Transform ActorForAccount to its information ActorInformation

    ```pycon
    >>> actor = ActorForAccount(actor="http://base.example/actor", name="Alice")
    >>> actor_to_information(actor)
    ActorInformation(id='http://base.example/actor', name='Alice')

    ```
    """
    return ActorInformation(id=actor.actor, name=actor.name)


async def create_information_response(
    account: Account, method_information: list[MethodInformationModel]
) -> InformationResponse:
    await account.fetch_related("actors")

    actor_ids = [
        actor_to_information(x)
        for x in account.actors
        if x.status == ActorStatus.active
    ]
    base_urls = await allowed_base_urls(account)

    return InformationResponse(
        account_name=account.name,
        base_urls=base_urls,
        actors=actor_ids,
        **protocol_and_backend(),
        method_information=method_information,
    )

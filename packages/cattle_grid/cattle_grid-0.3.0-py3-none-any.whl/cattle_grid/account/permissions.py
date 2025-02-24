from cattle_grid.dependencies.globals import global_container

from .account import list_permissions
from .models import Account


async def allowed_base_urls(account: Account) -> list[str]:
    """Returns the set of base_urls the account
    is allowed to use to create an actor"""
    settings = global_container.config
    await account.fetch_related("permissions")

    permissions = list_permissions(account)

    if "admin" in permissions:
        return settings.get("frontend", {}).get("base_urls", [])

    return sum(
        (
            settings.get("permissions", {}).get(p, {}).get("base_urls", [])
            for p in permissions
        ),
        [],
    )


async def can_create_actor_at_base_url(account: Account, base_url) -> bool:
    """Checks if the account is allowed to create an actor
    at the base url"""
    allowed_urls = await allowed_base_urls(account)

    return base_url in allowed_urls

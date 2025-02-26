"""Maps all of the inventories for a SciNote team."""

import logging

from cachetools import cached, TTLCache
from .inventory import Inventory
from ..client.api.inventory_client import InventoryClient

logger = logging.getLogger(__name__)

# How long we cache result from SciNote before refreshing.
CACHE_TIMEOUT_SECONDS = 120


class Inventories:
    """Maps all of the inventories for a SciNote team."""

    def __init__(self, client: InventoryClient):
        self.__client = client

    def inventory(self, name: str) -> Inventory:
        """Get the inventory by name."""

        inventories = self.__load_inventories()

        logger.debug(f'Checking for inventory {name}')
        if inventories.get(name) is None:
            raise ValueError(f'Inventory {name} not found')

        return inventories.get(name)

    def inventories(self) -> list[Inventory]:
        """Get all of the inventories."""
        inventories = self.__load_inventories()
        return [value for value in inventories.values()]

    @cached(cache=TTLCache(maxsize=1, ttl=CACHE_TIMEOUT_SECONDS))
    def __load_inventories(self):
        logger.debug('Loading all inventories')

        result = {}
        scinote_inventories = self.__client.get_inventories()
        for inventory in scinote_inventories:
            inventory_name = inventory.attributes.name.lower().replace(' ', '_')
            logger.debug(f'Adding inventory {inventory_name}')
            result[inventory_name] = Inventory(
                inventory_name,
                self.__client.column_client(inventory.id),
                self.__client.item_client(inventory.id),
            )

        return result

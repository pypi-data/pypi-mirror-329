"""Maps all of the inventories for a SciNote team."""

import logging

from .inventory import Inventory
from ..client.api.inventory_client import InventoryClient

logger = logging.getLogger(__name__)


class Inventories:
    """Maps all of the inventories for a SciNote team."""

    def __init__(self, client: InventoryClient):
        self.__client = client
        self.__inventories = {}

    def inventory(self, name: str) -> Inventory:
        """Get the inventory by name."""

        # TODO: Handle a new inventory being added after the initial load.
        # This is an edge case but we could do something with webhooks
        # to invalidate the cache.
        if self.__inventories.get(name) is None:
            self.__load_inventories()

        logger.debug(f'Checking again for inventory {name}')
        if self.__inventories.get(name) is None:
            raise ValueError(f'Inventory {name} not found')

        return self.__inventories.get(name)

    def inventories(self) -> list[Inventory]:
        """Get all of the inventories."""
        if not self.__inventories:
            self.__load_inventories()
        return [value for value in self.__inventories.values()]

    def __load_inventories(self):
        logger.debug('Loading all inventories')

        scinote_inventories = self.__client.get_inventories()
        for inventory in scinote_inventories:
            inventory_name = inventory.attributes.name.lower().replace(' ', '_')
            logger.debug(f'Adding inventory {inventory_name}')
            self.__inventories[inventory_name] = Inventory(
                inventory_name,
                self.__client.column_client(inventory.id),
                self.__client.item_client(inventory.id),
            )

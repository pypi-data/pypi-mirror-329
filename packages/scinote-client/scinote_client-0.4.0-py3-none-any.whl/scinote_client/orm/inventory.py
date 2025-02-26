"""ORM client for an specific inventory in SciNote."""

import logging

from cachetools import TTLCache

from .items import Item
from ..client.api.inventory_column_client import InventoryColumnClient
from ..client.api.inventory_item_client import InventoryItemClient
from ..client.models.inventory_cell import CreateInventoryCell

logger = logging.getLogger(__name__)

# How long we cache result from SciNote before refreshing.
CACHE_TIMEOUT_SECONDS = 120


class Inventory:
    """ORM client for a specific inventory in SciNote."""

    def __init__(
        self,
        name: str,
        column_client: InventoryColumnClient,
        item_client: InventoryItemClient,
    ):
        self.column_client = column_client
        self.item_client = item_client
        self.name = name
        self.__columns = {}
        self.__item_list = []
        self.__cache = TTLCache(maxsize=2, ttl=CACHE_TIMEOUT_SECONDS)

    @staticmethod
    def load_columns(func):
        """Load the columns for this inventory."""

        def wrapper(cls, *args, **kwargs):
            if 'columns' not in cls.__cache:
                columns = cls.column_client.get_columns()
                cls.__columns = {}
                for column in columns:
                    name = column.attributes.name.lower().replace(' ', '_')
                    cls.__columns[name] = column
                cls.__cache['columns'] = True
            return func(cls, *args, **kwargs)

        return wrapper

    @staticmethod
    def load_items(func):
        """Load the items for this inventory."""

        def wrapper(cls, *args, **kwargs):
            if 'items' not in cls.__cache:
                items = cls.item_client.get_items()
                cls.__item_list = []
                for item in items:
                    cls.__item_list.append(
                        Item(
                            item.id,
                            item.attributes.name,
                            item.attributes.created_at,
                            cls.item_client,
                            cls.__columns,
                            item.inventory_cells,
                        )
                    )
                cls.__cache['items'] = True
            return func(cls, *args, **kwargs)

        return wrapper

    @load_columns
    @load_items
    def items(self) -> list[Item]:
        """Get the items for this inventory."""
        return self.__item_list

    @load_columns
    @load_items
    def match(self, **kwargs) -> list[Item]:
        """Return matching items from this inventory."""
        return [item for item in self.__item_list if item.match(**kwargs)]

    @load_columns
    def columns(self):
        """Get the columns for this inventory."""
        return [column for column in self.__columns.values()]

    @load_columns
    def create_item(self, name: str, **kwargs) -> Item:
        """Create a new item in this inventory."""
        cells = []
        for key, value in kwargs.items():
            if key not in self.__columns:
                raise ValueError(f'Column {key} does not exist in inventory.')

            column = self.__columns[key]
            cells.append(CreateInventoryCell(value=value, column_id=column.id))

        item = self.item_client.create_item(name, cells)

        new_item = Item(
            item.id,
            item.attributes.name,
            item.attributes.created_at,
            self.item_client,
            self.__columns,
            item.inventory_cells,
        )
        self.__item_list.append(new_item)
        return new_item

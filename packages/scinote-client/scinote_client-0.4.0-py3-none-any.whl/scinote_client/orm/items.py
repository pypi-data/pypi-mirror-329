"""Maps a SciNote item to an ORM item."""

import logging

from datetime import datetime

from .cell import Cell
from ..client.api.inventory_item_client import InventoryItemClient
from ..client.models.inventory_cell import InventoryCell, Attributes

logger = logging.getLogger(__name__)
"""
An item is a complete row in the inventory.

When SciNote returns an item, the values are mapped to a column ID. We need to
do this mapping here using the columns for the inventory and the values that
are passed into the constructor.
"""


class Item:
    """Maps a SciNote item to an ORM item."""

    def __init__(
        self,
        id: str,
        name: str,
        created_at: datetime,
        item_client: InventoryItemClient,
        columns: dict,
        values: list[InventoryCell],
    ):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.item_client = item_client
        self.column_ids = {}
        self.column_names = {}
        self.__cells = {}

        logger.debug(f'Columns: {columns}')
        logger.debug(f'Values: {values}')

        # Create a map of column ids to names and vice versa.
        for index, (key, value) in enumerate(columns.items()):
            name = key.lower().replace(' ', '_')
            self.column_ids[value.id] = name
            self.column_names[name] = value.id

        # For each incoming value, map it to the column name. There is added
        # complexity as the name of the field that is the value of the cell
        # is dependent on the type of the column.
        for value in values:
            column_id = str(value.attributes.column_id)
            column_name = self.column_ids[column_id]
            self.__cells[column_name] = Cell(
                value.id,
                value.attributes,
                item_client.cell_client(self.id),
            )

        # SciNote will only return values if they are not empty. We need to
        # create empty cells for the columns that are not present.
        empty_columns = set(self.column_names.keys()) - set(self.__cells.keys())
        logger.debug(f'Empty columns: {empty_columns}')
        for column_name in empty_columns:
            # Get metadata for the missing column.
            column = columns[column_name]
            self.__cells[column_name] = Cell(
                None,  # No id for cells that do not exist.
                Attributes(
                    column_id=column.id,
                    value_type=column.attributes.data_type,
                ),
                item_client.cell_client(self.id),
            )

    def cell(self, name) -> Cell:
        """Get the item by name."""
        if self.column_names.get(name) is None:
            raise ValueError(f'Item {name} not found')
        return self.__cells.get(name)

    def cells(self) -> list[Cell]:
        """Get all of the cells."""
        return [value for value in self.__cells.values()]

    def match(self, **kwargs) -> bool:
        """Match the item against the given values."""
        for key, value in kwargs.items():
            if key == 'name':
                if self.name != value:
                    return False
                continue
            if key == 'id':
                if self.id != value:
                    return False
                continue

            if key not in self.column_names:
                logger.warning(f'Column {key} not found in item')
                return False

            if not self.cell(key).match(value):
                return False

        return True

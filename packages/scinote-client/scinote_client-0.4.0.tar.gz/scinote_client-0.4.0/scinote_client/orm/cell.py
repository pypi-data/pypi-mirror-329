"""ORM client for a specific cell in an inventory in SciNote."""

import logging

from ..client.api.inventory_cell_client import InventoryCellClient
from ..client.models.inventory_cell import (
    CreateInventoryCell,
    UpdateInventoryCell,
    Attributes,
)

logger = logging.getLogger(__name__)


class Cell:
    """ORM client for a specific cell in an inventory in SciNote."""

    def __init__(
        self, cell_id: int, attributes: Attributes, client: InventoryCellClient
    ):
        self.cell_id = cell_id
        self.attributes = attributes
        self.__client = client

    def value(self):
        """Get the value of the cell."""
        logger.debug(f'Getting value for cell {self.attributes}')

        # Empty cells will not have a value.
        if self.attributes.value is None:
            return None

        match self.attributes.value_type:
            case 'text':
                return self.attributes.value.text
            case 'number':
                return self.attributes.value.data
            case 'list':
                return self.attributes.value.inventory_list_item_name
            case 'date_time':
                return self.attributes.value.date_time
            case 'date':
                return self.attributes.value.date
            case _:
                raise ValueError(
                    f'Unknown value type {self.attributes.value_type}'
                )

    def update_value(self, value: str):
        """Update the value stored in cell."""
        logger.debug(f'Updating value for cell {self.attributes}')
        # We need to check if we are creating a new value or updating an
        # existing one.

        if self.attributes.value is None:
            self.__do_create_cell(value)
        else:
            self.__do_update_cell(value)

    def __do_create_cell(self, value: str):
        try:
            result = self.__client.create_cell(
                CreateInventoryCell(
                    value=value, column_id=self.attributes.column_id
                )
            )
            if result:
                self.cell_id = result.id
                self.attributes = result.attributes
        except Exception as e:
            logger.error(f'Failed to create cell value={value}: {e}')
            raise

    def __do_update_cell(self, value: str):
        try:
            result = self.__client.update_cell(
                UpdateInventoryCell(
                    id=self.cell_id,
                    value=value,
                    column_id=self.attributes.column_id,
                )
            )
            if result:
                self.attributes = result.attributes
        except Exception as e:
            logger.error(f'Failed to update cell {self.cell_id}: {e}')
            raise

    def match(self, value: str) -> bool:
        """Check if the value of the cell matches the supplied string."""

        if self.attributes.value is None:
            return False

        match self.attributes.value_type:
            case 'text':
                return value == self.attributes.value.text
            case 'number':
                return value == self.attributes.value.data
            case 'list':
                return value == self.attributes.value.inventory_list_item_name
            case 'date_time':
                return value == self.attributes.value.date_time
            case 'date':
                return value == self.attributes.value.date
            case _:
                raise ValueError(
                    f'Unknown value type {self.attributes.value_type}'
                )

        return False

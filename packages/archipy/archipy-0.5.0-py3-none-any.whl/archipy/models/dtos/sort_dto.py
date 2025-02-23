from enum import Enum
from typing import Generic, Self, TypeVar

from pydantic import BaseModel

from archipy.models.types.sort_order_type import SortOrderType

# Generic types
T = TypeVar('T', bound=Enum)


class SortDTO(BaseModel, Generic[T]):
    column: T | str
    order: SortOrderType = SortOrderType.DESCENDING

    @classmethod
    def default(cls) -> Self:
        return cls(column="created_at", order=SortOrderType.DESCENDING)

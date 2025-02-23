from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel

from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO

# Generic types
T = TypeVar('T', bound=Enum)


class SearchInputDTO(BaseModel, Generic[T]):
    pagination: PaginationDTO | None = None
    sort_info: SortDTO[T] | None = None

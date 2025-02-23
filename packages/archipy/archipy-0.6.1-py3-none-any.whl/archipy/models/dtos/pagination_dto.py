from enum import Enum
from typing import ClassVar, Self, TypeVar

from pydantic import Field, PositiveInt, model_validator

from archipy.models.dtos.base_dtos import BaseDTO

# Generic types
T = TypeVar("T", bound=Enum)


class PaginationDTO(BaseDTO):
    page: PositiveInt = Field(default=1, ge=1)
    page_size: PositiveInt = Field(default=10, le=100)

    MAX_ITEMS: ClassVar = 10000

    @model_validator(mode="after")
    def validate_pagination(cls, model: Self) -> Self:
        total_items = model.page * model.page_size
        if total_items > cls.MAX_ITEMS:
            raise ValueError(
                f"Pagination limit exceeded. "
                f"Requested {total_items} items, but the maximum is {cls.MAX_ITEMS}. "
                f"Try reducing page size or requesting a lower page number.",
            )
        return model

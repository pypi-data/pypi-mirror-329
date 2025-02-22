from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import ClassVar, Generic, Self, TypeVar

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StrictInt, field_validator, model_validator

from archipy.models.types import SortOrderType

# Generic types
T = TypeVar('T', bound=Enum)


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_default=True,
        from_attributes=True,
        frozen=True,
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
    )


class SortDTO(BaseModel, Generic[T]):
    column: T | str
    order: SortOrderType = SortOrderType.DESCENDING

    @classmethod
    def default(cls) -> Self:
        return cls(column="created_at", order=SortOrderType.DESCENDING)


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


class SearchInputDTO(BaseModel, Generic[T]):
    pagination: PaginationDTO | None = None
    sort_info: SortDTO[T] | None = None


class RangeDTO(BaseDTO):
    from_: Decimal | None = None
    to: Decimal | None = None

    @field_validator("from_", "to", mode="before")
    def convert_to(cls, value: Decimal | str | None) -> Decimal | None:
        if value is None:
            return value
        if not (isinstance(value, Decimal | str)):
            raise ValueError("Decimal input should be str or decimal.")
        return Decimal(value)

    @model_validator(mode="after")
    def validate_range(cls, model: Self) -> Self:
        if model.from_ and model.to and model.from_ >= model.to:
            raise ValueError("from_ can`t be bigger than to")
        return model


class IntegerRangeDTO(BaseDTO):
    from_: StrictInt | None = None
    to: StrictInt | None = None

    @model_validator(mode="after")
    def validate_range(cls, model: Self) -> Self:
        if model.from_ and model.to and model.from_ > model.to:
            raise ValueError("from_ can`t be bigger than to")
        return model


class DateRangeDTO(BaseDTO):
    from_: date | None = None
    to: date | None = None

    @model_validator(mode="after")
    def validate_range(cls, model: Self) -> Self:
        if model.from_ and model.to and model.from_ > model.to:
            raise ValueError("from_ can`t be bigger than to")
        return model


class DatetimeRangeDTO(BaseDTO):
    from_: datetime | None = None
    to: datetime | None = None

    @model_validator(mode="after")
    def validate_range(cls, model: Self) -> Self:
        if model.from_ and model.to and model.from_ > model.to:
            raise ValueError("from_ can`t be bigger than to")
        return model

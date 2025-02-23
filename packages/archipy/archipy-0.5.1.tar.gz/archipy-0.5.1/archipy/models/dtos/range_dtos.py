from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Self, TypeVar

from pydantic import StrictInt, field_validator, model_validator

from archipy.models.dtos.base_dtos import BaseDTO

# Generic types
T = TypeVar("T", bound=Enum)


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

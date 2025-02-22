from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, Synonym

from archipy.helpers.utils.base_utils import BaseUtils

PK_COLUMN_NAME = "pk_uuid"


class BaseEntity(DeclarativeBase):
    """Base entities class for all models with automatic timestamps."""

    __abstract__ = True

    created_at: Mapped[datetime] = Column(DateTime(), server_default="DEFAULT", nullable=False)

    @classmethod
    def _is_abstract(cls) -> bool:
        return (not hasattr(cls, "__tablename__")) and cls.__abstract__

    def __init_subclass__(cls, **kw: Any) -> None:
        if cls._is_abstract():
            return None
        cls._validate_pk_column()
        super().__init_subclass__(**kw)

    @classmethod
    def _validate_pk_column(cls) -> None:
        if not hasattr(cls, PK_COLUMN_NAME):
            raise AttributeError(f"Child class {cls.__name__} must have {PK_COLUMN_NAME}")
        pk_column = getattr(cls, PK_COLUMN_NAME)
        if not isinstance(pk_column, Synonym):
            raise AttributeError(f"{PK_COLUMN_NAME} must be a sqlalchemy.orm.Synonym type")


class EntityAttributeChecker:
    """Utility for checking models attributes."""

    required_any: list[list[str]] = []

    @classmethod
    def validate(cls, base_class) -> None:
        """Ensure at least one of the specified attributes is present."""
        for attrs in cls.required_any:
            if not any(hasattr(base_class, attr) for attr in attrs):
                raise AttributeError(f"One of {attrs} must be defined in {base_class.__name__}")


class DeletableMixin:
    """Mixin to support a deletable flag on models."""

    __abstract__ = True

    is_deleted = Column(Boolean, default=False, nullable=False)


class AdminMixin(EntityAttributeChecker):
    """Mixin for handling admin-related attributes."""

    __abstract__ = True
    required_any = [["created_by_admin", "created_by_admin_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        cls.validate(cls)
        super().__init_subclass__(**kw)


class ManagerMixin(EntityAttributeChecker):
    """Mixin to enforce manager-related attributes."""

    __abstract__ = True
    required_any = [["created_by", "created_by_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        cls.validate(cls)
        super().__init_subclass__(**kw)


class UpdatableAdminMixin(EntityAttributeChecker):
    """Mixin for models updatable by admin."""

    __abstract__ = True
    required_any = [["updated_by_admin", "updated_by_admin_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        cls.validate(cls)
        super().__init_subclass__(**kw)


class UpdatableManagerMixin(EntityAttributeChecker):
    """Mixin for models updatable by managers."""

    __abstract__ = True
    required_any = [["updated_by", "updated_by_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        cls.validate(cls)
        super().__init_subclass__(**kw)


class UpdatableMixin:
    """Mixin to add updatable timestamp functionality."""

    __abstract__ = True
    updated_at = Column(
        DateTime(),
        default=BaseUtils.get_datetime_now,
        nullable=False,
        onupdate=BaseUtils.get_datetime_now,
    )


# Composite entities types extending BaseEntity with various mixins
class UpdatableEntity(BaseEntity, UpdatableMixin):
    __abstract__ = True


class DeletableEntity(BaseEntity, DeletableMixin):
    __abstract__ = True


class UpdatableDeletableEntity(BaseEntity, UpdatableMixin, DeletableMixin):
    __abstract__ = True


class AdminEntity(BaseEntity, AdminMixin):
    __abstract__ = True


class ManagerEntity(BaseEntity, ManagerMixin):
    __abstract__ = True


class UpdatableAdminEntity(BaseEntity, UpdatableMixin, AdminMixin, UpdatableAdminMixin):
    __abstract__ = True


class UpdatableManagerEntity(BaseEntity, UpdatableMixin, ManagerMixin, UpdatableManagerMixin):
    __abstract__ = True


class UpdatableManagerAdminEntity(
    BaseEntity,
    UpdatableMixin,
    ManagerMixin,
    AdminMixin,
    UpdatableManagerMixin,
    UpdatableAdminMixin,
):
    __abstract__ = True


class UpdatableDeletableAdminEntity(BaseEntity, UpdatableMixin, AdminMixin, UpdatableAdminMixin, DeletableMixin):
    __abstract__ = True


class UpdatableDeletableManagerEntity(BaseEntity, UpdatableMixin, ManagerMixin, UpdatableManagerMixin, DeletableMixin):
    __abstract__ = True


class UpdatableDeletableManagerAdminEntity(
    BaseEntity,
    UpdatableMixin,
    ManagerMixin,
    AdminMixin,
    UpdatableManagerMixin,
    UpdatableAdminMixin,
    DeletableMixin,
):
    __abstract__ = True

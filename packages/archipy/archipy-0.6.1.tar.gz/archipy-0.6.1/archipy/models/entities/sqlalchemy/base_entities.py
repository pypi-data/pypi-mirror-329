from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, Synonym

from archipy.helpers.utils.base_utils import BaseUtils

PK_COLUMN_NAME = "pk_uuid"


class BaseEntity(DeclarativeBase):
    """Base class for all SQLAlchemy models with automatic timestamps.

    This class serves as the base for all entities in the application. It provides
    common functionality such as automatic timestamping for `created_at` and
    validation for the primary key column.

    Attributes:
        created_at (Mapped[datetime]): Timestamp indicating when the entity was created.
    """

    __abstract__ = True

    created_at: Mapped[datetime] = Column(DateTime(), server_default="DEFAULT", nullable=False)

    @classmethod
    def _is_abstract(cls) -> bool:
        """Check if the class is abstract.

        Returns:
            bool: True if the class is abstract, False otherwise.
        """
        return (not hasattr(cls, "__tablename__")) and cls.__abstract__

    def __init_subclass__(cls, **kw: Any) -> None:
        """Validate the subclass during initialization.

        Args:
            **kw: Additional keyword arguments passed to the subclass.

        Raises:
            AttributeError: If the subclass does not have the required primary key column.
        """
        if cls._is_abstract():
            return
        cls._validate_pk_column()
        super().__init_subclass__(**kw)

    @classmethod
    def _validate_pk_column(cls) -> None:
        """Validate that the subclass has the required primary key column.

        Raises:
            AttributeError: If the primary key column is missing or invalid.
        """
        if not hasattr(cls, PK_COLUMN_NAME):
            raise AttributeError(f"Child class {cls.__name__} must have {PK_COLUMN_NAME}")
        pk_column = getattr(cls, PK_COLUMN_NAME)
        if not isinstance(pk_column, Synonym):
            raise AttributeError(f"{PK_COLUMN_NAME} must be a sqlalchemy.orm.Synonym type")


class EntityAttributeChecker:
    """Utility class for validating model attributes.

    This class provides functionality to ensure that at least one of the specified
    attributes is present in a model.

    Attributes:
        required_any (list[list[str]]): A list of lists, where each inner list contains
            attribute names. At least one attribute from each inner list must be present.
    """

    required_any: list[list[str]] = []

    @classmethod
    def validate(cls, base_class) -> None:
        """Validate that at least one of the required attributes is present.

        Args:
            base_class: The class to validate.

        Raises:
            AttributeError: If none of the required attributes are present.
        """
        for attrs in cls.required_any:
            if not any(hasattr(base_class, attr) for attr in attrs):
                raise AttributeError(f"One of {attrs} must be defined in {base_class.__name__}")


class DeletableMixin:
    """Mixin to add a deletable flag to models.

    This mixin adds a `is_deleted` column to indicate whether the entity has been
    soft-deleted.

    Attributes:
        is_deleted (Column[Boolean]): Flag indicating if the entity is deleted.
    """

    __abstract__ = True

    is_deleted = Column(Boolean, default=False, nullable=False)


class AdminMixin(EntityAttributeChecker):
    """Mixin for models with admin-related attributes.

    This mixin ensures that at least one of the admin-related attributes is present.

    Attributes:
        required_any (list[list[str]]): Specifies the required admin-related attributes.
    """

    __abstract__ = True
    required_any = [["created_by_admin", "created_by_admin_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        """Validate the subclass during initialization.

        Args:
            **kw: Additional keyword arguments passed to the subclass.
        """
        cls.validate(cls)
        super().__init_subclass__(**kw)


class ManagerMixin(EntityAttributeChecker):
    """Mixin for models with manager-related attributes.

    This mixin ensures that at least one of the manager-related attributes is present.

    Attributes:
        required_any (list[list[str]]): Specifies the required manager-related attributes.
    """

    __abstract__ = True
    required_any = [["created_by", "created_by_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        """Validate the subclass during initialization.

        Args:
            **kw: Additional keyword arguments passed to the subclass.
        """
        cls.validate(cls)
        super().__init_subclass__(**kw)


class UpdatableAdminMixin(EntityAttributeChecker):
    """Mixin for models updatable by admin.

    This mixin ensures that at least one of the admin-related update attributes is present.

    Attributes:
        required_any (list[list[str]]): Specifies the required admin-related update attributes.
    """

    __abstract__ = True
    required_any = [["updated_by_admin", "updated_by_admin_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        """Validate the subclass during initialization.

        Args:
            **kw: Additional keyword arguments passed to the subclass.
        """
        cls.validate(cls)
        super().__init_subclass__(**kw)


class UpdatableManagerMixin(EntityAttributeChecker):
    """Mixin for models updatable by managers.

    This mixin ensures that at least one of the manager-related update attributes is present.

    Attributes:
        required_any (list[list[str]]): Specifies the required manager-related update attributes.
    """

    __abstract__ = True
    required_any = [["updated_by", "updated_by_uuid"]]

    def __init_subclass__(cls, **kw: Any) -> None:
        """Validate the subclass during initialization.

        Args:
            **kw: Additional keyword arguments passed to the subclass.
        """
        cls.validate(cls)
        super().__init_subclass__(**kw)


class UpdatableMixin:
    """Mixin to add updatable timestamp functionality.

    This mixin adds an `updated_at` column to track the last update time of the entity.

    Attributes:
        updated_at (Column[DateTime]): Timestamp indicating when the entity was last updated.
    """

    __abstract__ = True
    updated_at = Column(
        DateTime(),
        default=BaseUtils.get_datetime_now,
        nullable=False,
        onupdate=BaseUtils.get_datetime_now,
    )


# Composite entities types extending BaseEntity with various mixins
class UpdatableEntity(BaseEntity, UpdatableMixin):
    """Base class for entities that support updating timestamps."""

    __abstract__ = True


class DeletableEntity(BaseEntity, DeletableMixin):
    """Base class for entities that support soft deletion."""

    __abstract__ = True


class UpdatableDeletableEntity(BaseEntity, UpdatableMixin, DeletableMixin):
    """Base class for entities that support updating timestamps and soft deletion."""

    __abstract__ = True


class AdminEntity(BaseEntity, AdminMixin):
    """Base class for entities with admin-related attributes."""

    __abstract__ = True


class ManagerEntity(BaseEntity, ManagerMixin):
    """Base class for entities with manager-related attributes."""

    __abstract__ = True


class UpdatableAdminEntity(BaseEntity, UpdatableMixin, AdminMixin, UpdatableAdminMixin):
    """Base class for entities updatable by admin with timestamps."""

    __abstract__ = True


class UpdatableManagerEntity(BaseEntity, UpdatableMixin, ManagerMixin, UpdatableManagerMixin):
    """Base class for entities updatable by managers with timestamps."""

    __abstract__ = True


class UpdatableManagerAdminEntity(
    BaseEntity,
    UpdatableMixin,
    ManagerMixin,
    AdminMixin,
    UpdatableManagerMixin,
    UpdatableAdminMixin,
):
    """Base class for entities updatable by both managers and admins with timestamps."""

    __abstract__ = True


class UpdatableDeletableAdminEntity(BaseEntity, UpdatableMixin, AdminMixin, UpdatableAdminMixin, DeletableMixin):
    """Base class for entities updatable by admin with timestamps and soft deletion."""

    __abstract__ = True


class UpdatableDeletableManagerEntity(BaseEntity, UpdatableMixin, ManagerMixin, UpdatableManagerMixin, DeletableMixin):
    """Base class for entities updatable by managers with timestamps and soft deletion."""

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
    """Base class for entities updatable by both managers and admins with timestamps and soft deletion."""

    __abstract__ = True

from enum import Enum
from typing import Any, Type, Union, override
from uuid import UUID

from sqlalchemy import Delete, Executable, Result, ScalarResult, Update, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, Session
from sqlalchemy.sql import Select

from archipy.adapters.orm.sqlalchemy.session_manager_adapters import AsyncSessionManagerAdapter, SessionManagerAdapter
from archipy.adapters.orm.sqlalchemy.sqlalchemy_ports import AnyExecuteParams, AsyncSqlAlchemyPort, SqlAlchemyPort
from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import SqlAlchemyConfig
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.entities import BaseEntity
from archipy.models.exceptions import InvalidEntityTypeException
from archipy.models.types.base_types import FilterOperationType
from archipy.models.types.sort_order_type import SortOrderType


class SqlAlchemyFilterMixin:
    @staticmethod
    def _apply_filter(
        query: Select | Update | Delete,
        field: InstrumentedAttribute,
        value: Any,
        operation: FilterOperationType,
    ) -> Select | Update | Delete:
        if value is not None or operation in [FilterOperationType.IS_NULL, FilterOperationType.IS_NOT_NULL]:
            if operation == FilterOperationType.EQUAL:
                return query.where(field == value)
            elif operation == FilterOperationType.NOT_EQUAL:
                return query.where(field != value)
            elif operation == FilterOperationType.LESS_THAN:
                return query.where(field < value)
            elif operation == FilterOperationType.LESS_THAN_OR_EQUAL:
                return query.where(field <= value)
            elif operation == FilterOperationType.GREATER_THAN:
                return query.where(field > value)
            elif operation == FilterOperationType.GREATER_THAN_OR_EQUAL:
                return query.where(field >= value)
            elif operation == FilterOperationType.IN_LIST:
                return query.where(field.in_(value))
            elif operation == FilterOperationType.NOT_IN_LIST:
                return query.where(~field.in_(value))
            elif operation == FilterOperationType.LIKE:
                return query.where(field.like(f'%{value}%'))
            elif operation == FilterOperationType.ILIKE:
                return query.where(field.ilike(f'%{value}%'))
            elif operation == FilterOperationType.STARTS_WITH:
                return query.where(field.startswith(value))
            elif operation == FilterOperationType.ENDS_WITH:
                return query.where(field.endswith(value))
            elif operation == FilterOperationType.CONTAINS:
                return query.where(field.contains(value))
            elif operation == FilterOperationType.IS_NULL:
                return query.where(field.is_(None))
            elif operation == FilterOperationType.IS_NOT_NULL:
                return query.where(field.isnot(None))
        return query


class SqlAlchemyPaginationMixin:
    @staticmethod
    def _apply_pagination(query: Select, pagination: PaginationDTO | None) -> Select:
        if pagination is None:
            return query
        return query.limit(pagination.page_size).offset((pagination.page - 1) * pagination.page_size)


class SqlAlchemySortMixin:
    @staticmethod
    def _apply_sorting(entity: Type[BaseEntity], query: Select, sort_info: SortDTO | None) -> Select:
        if sort_info is None:
            return query
        if isinstance(sort_info.column, str):
            sort_column = getattr(entity, sort_info.column)
        elif isinstance(sort_info.column, Enum):
            sort_column = getattr(entity, sort_info.column.name.lower())
        else:
            sort_column = sort_info.column

        if sort_info.order == SortOrderType.ASCENDING:
            return query.order_by(sort_column.asc())
        else:
            return query.order_by(sort_column.desc())


class SqlAlchemyAdapter(SqlAlchemyPort, SqlAlchemyPaginationMixin, SqlAlchemySortMixin):
    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        configs: SqlAlchemyConfig = BaseConfig.global_config().SQLALCHEMY if orm_config is None else orm_config
        self.session_manager = SessionManagerAdapter(configs)

    @override
    def execute_search_query(
        self,
        entity: Type[BaseEntity],
        query: Select,
        pagination: PaginationDTO | None = None,
        sort_info: SortDTO | None = SortDTO.default(),
    ) -> tuple[list[BaseEntity], int]:
        try:
            session = self.get_session()
            sorted_query = self._apply_sorting(entity, query, sort_info)
            paginated_query = self._apply_pagination(sorted_query, pagination)

            results = session.execute(paginated_query)
            results = results.scalars().all()

            count_query = select(func.count()).select_from(query.subquery())
            total_count = session.execute(count_query).scalar_one()
            return results, total_count
        except Exception as e:
            raise RuntimeError(f"Database query failed: {e!s}") from e

    @override
    def get_session(self) -> Session:
        return self.session_manager.get_session()

    @override
    def create(self, entity: BaseEntity) -> BaseEntity | None:
        if not isinstance(entity, BaseEntity):
            raise InvalidEntityTypeException(entity, BaseEntity)
        session: Session = self.get_session()
        session.add(entity)
        session.flush()
        return entity

    @override
    def bulk_create(self, entities: list[BaseEntity]) -> list[BaseEntity] | None:
        session = self.get_session()
        session.add_all(entities)
        session.flush()
        return entities

    @override
    def get_by_uuid(self, entity_type: type, entity_uuid: UUID):
        if not issubclass(entity_type, BaseEntity):
            raise InvalidEntityTypeException(entity_type, BaseEntity)
        if not isinstance(entity_uuid, UUID):
            raise InvalidEntityTypeException(entity_uuid, UUID)
        session = self.get_session()
        return session.get(entity_type, entity_uuid)

    @override
    def delete(self, entity: BaseEntity) -> None:
        if not isinstance(entity, BaseEntity):
            raise InvalidEntityTypeException(entity, BaseEntity)
        session = self.get_session()
        session.delete(entity)

    @override
    def bulk_delete(self, entities: list[BaseEntity]) -> None:
        for entity in entities:
            self.delete(entity)

    @override
    def execute(self, statement: Executable, params: AnyExecuteParams | None = None):
        session = self.get_session()
        return session.execute(statement, params)

    @override
    def scalars(self, statement: Executable, params: AnyExecuteParams | None = None):
        session = self.get_session()
        return session.scalars(statement, params)


class AsyncSqlAlchemyAdapter(AsyncSqlAlchemyPort, SqlAlchemyPaginationMixin, SqlAlchemySortMixin):
    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        configs: SqlAlchemyConfig = BaseConfig.global_config().SQLALCHEMY if orm_config is None else orm_config
        self.session_manager = AsyncSessionManagerAdapter(configs)

    @override
    async def execute_search_query(
        self,
        entity: Type[BaseEntity],
        query: Select,
        pagination: PaginationDTO | None,
        sort_info: SortDTO | None = SortDTO.default(),
    ) -> tuple[list[BaseEntity], int]:
        try:
            session = self.get_session()
            sorted_query = self._apply_sorting(entity, query, sort_info)
            paginated_query = self._apply_pagination(sorted_query, pagination)

            results = await session.execute(paginated_query)
            results = results.scalars().all()

            count_query = select(func.count()).select_from(query.subquery())
            total_count = await session.execute(count_query)
            total_count = total_count.scalar_one()
            return results, total_count
        except Exception as e:
            raise RuntimeError(f"Database query failed: {e!s}") from e

    @override
    def get_session(self) -> AsyncSession:
        return self.session_manager.get_session()

    @override
    async def create(self, entity: BaseEntity) -> BaseEntity | None:
        if not isinstance(entity, BaseEntity):
            raise InvalidEntityTypeException(entity, BaseEntity)
        session: AsyncSession = self.get_session()
        session.add(entity)
        await session.flush()
        return entity

    @override
    async def bulk_create(self, entities: list[BaseEntity]) -> list[BaseEntity] | None:
        session = self.get_session()
        session.add_all(entities)
        await session.flush()
        return entities

    @override
    async def get_by_uuid(self, entity_type: type, entity_uuid: UUID) -> Union[Any, None]:
        if not issubclass(entity_type, BaseEntity):
            raise InvalidEntityTypeException(entity_type, BaseEntity)
        if not isinstance(entity_uuid, UUID):
            raise InvalidEntityTypeException(entity_uuid, UUID)
        session = self.get_session()
        return await session.get(entity_type, entity_uuid)

    @override
    async def delete(self, entity: BaseEntity) -> None:
        if not isinstance(entity, BaseEntity):
            raise InvalidEntityTypeException(entity, BaseEntity)
        session = self.get_session()
        await session.delete(entity)

    @override
    async def bulk_delete(self, entities: list[BaseEntity]) -> None:
        for entity in entities:
            await self.delete(entity)

    @override
    async def execute(self, statement: Executable, params: AnyExecuteParams | None = None) -> Result[Any]:
        session = self.get_session()
        return await session.execute(statement, params)

    @override
    async def scalars(self, statement: Executable, params: AnyExecuteParams | None = None) -> ScalarResult[Any]:
        session = self.get_session()
        return await session.scalars(statement, params)

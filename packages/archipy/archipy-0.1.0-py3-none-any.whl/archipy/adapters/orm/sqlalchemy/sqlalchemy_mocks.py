from archipy.adapters.orm.sqlalchemy.session_manager_mocks import AsyncSessionManagerMock, SessionManagerMock
from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import AsyncSqlAlchemyAdapter, SqlAlchemyAdapter
from archipy.configs.config_template import SqlAlchemyConfig


class SqlAlchemyMock(SqlAlchemyAdapter):
    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        if orm_config:
            configs: SqlAlchemyConfig = orm_config
        else:
            configs: SqlAlchemyConfig = SqlAlchemyConfig(
                DRIVER_NAME="sqlite",
                DATABASE=":memory:",
                ISOLATION_LEVEL=None,
                PORT=None,
            )
        self.session_manager = SessionManagerMock(configs)


class AsyncSqlAlchemyMock(AsyncSqlAlchemyAdapter):
    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        if orm_config:
            configs: SqlAlchemyConfig = orm_config
        else:
            configs: SqlAlchemyConfig = SqlAlchemyConfig(
                DRIVER_NAME="sqlite+aiosqlite",
                DATABASE=":memory:",
                ISOLATION_LEVEL=None,
                PORT=None,
            )
        self.session_manager = AsyncSessionManagerMock(configs)

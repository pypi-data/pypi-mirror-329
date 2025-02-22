from typing import Generic, Self, TypeVar

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from archipy.configs.config_template import (
    AuthConfig,
    DatetimeConfig,
    ElasticSearchAPMConfig,
    ElasticSearchConfig,
    EmailConfig,
    FastAPIConfig,
    FileConfig,
    GrpcConfig,
    KafkaConfig,
    KavenegarConfig,
    KeycloakConfig,
    PrometheusConfig,
    RedisConfig,
    SentryConfig,
    SqlAlchemyConfig,
)
from archipy.configs.environment_type import EnvironmentType

"""

Priority :
            1. pypoject.toml [tool.configs]
            2. configs.toml or other toml file init
            3. .env file
            4. os level environment variable
            5. class field value
"""
R = TypeVar('R')  # Runtime Config


class BaseConfig(BaseSettings, Generic[R]):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        pyproject_toml_depth=3,
        env_file=".env",
        pyproject_toml_table_header=("tool", "configs"),
        extra="ignore",
        env_nested_delimiter="__",
        env_ignore_empty=True,
    )

    __global_config: Self | None = None

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            file_secret_settings,
            PyprojectTomlConfigSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            init_settings,
        )

    AUTH: AuthConfig = AuthConfig()
    DATETIME: DatetimeConfig = DatetimeConfig()
    ELASTIC: ElasticSearchConfig = ElasticSearchConfig()
    ELASTIC_APM: ElasticSearchAPMConfig = ElasticSearchAPMConfig()
    EMAIL: EmailConfig = EmailConfig()
    ENVIRONMENT: EnvironmentType = EnvironmentType.LOCAL
    FASTAPI: FastAPIConfig = FastAPIConfig()
    FILE: FileConfig = FileConfig()
    GRPC: GrpcConfig = GrpcConfig()
    KAFKA: KafkaConfig = KafkaConfig()
    KAVENEGAR: KavenegarConfig = KavenegarConfig()
    KEYCLOAK: KeycloakConfig = KeycloakConfig()
    PROMETHEUS: PrometheusConfig = PrometheusConfig()
    REDIS: RedisConfig = RedisConfig()
    SENTRY: SentryConfig = SentryConfig()
    SQLALCHEMY: SqlAlchemyConfig = SqlAlchemyConfig()

    def customize(self) -> None: ...

    @classmethod
    def global_config(cls) -> R:
        if cls.__global_config is None:
            raise AssertionError("You should set global configs with  BaseConfig.set_global(MyConfig())")
        return cls.__global_config

    @classmethod
    def set_global(cls, config: R) -> None:
        config.customize()
        cls.__global_config = config

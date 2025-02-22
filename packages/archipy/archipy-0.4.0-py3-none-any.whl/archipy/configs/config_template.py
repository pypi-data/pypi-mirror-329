from typing import Literal

from pydantic import BaseModel, Field, SecretStr


class ElasticSearchConfig(BaseModel):
    SEARCH_HOSTS: list = []
    SEARCH_HTTP_USER_NAME: str | None = None
    SEARCH_HTTP_PASSWORD: str | None = None
    SEARCH_HTTPS_VERIFY_CERTS: bool = False
    SEARCH_KWARG: dict = {}
    SEARCH_BATCH_INTERVAL_THRESHOLD_IN_SECONDS: int = 1
    SEARCH_BATCH_DOC_COUNT_THRESHOLD: int = 500


class ElasticSearchAPMConfig(BaseModel):
    API_REQUEST_SIZE: str = "768kb"
    API_REQUEST_TIME: str = "10s"
    AUTO_LOG_STACKS: bool = True
    CAPTURE_BODY: str = "off"
    CAPTURE_HEADERS: bool = False
    COLLECT_LOCAL_VARIABLES: str = "errors"
    IS_ENABLED: bool = False
    ENVIRONMENT: str | None = None
    LOG_FILE: str = ""
    LOG_FILE_SIZE: str = "1mb"
    RECORDING: bool = True
    SECRET_TOKEN: str | None = None
    SERVER_TIMEOUT: str = "5s"
    SERVER_URL: str | None = None
    SERVICE_NAME: str = "unknown-python-service"
    SERVICE_VERSION: str | None = None
    TRANSACTION_SAMPLE_RATE: str = "0.001"
    API_KEY: str | None = None


class FastAPIConfig(BaseModel):
    PROJECT_NAME: str = "project_name"
    API_PREFIX: str = "/api"

    ACCESS_LOG: bool = True
    BACKLOG: int = 2048
    DATE_HEADER: bool = True
    FORWARDED_ALLOW_IPS: list | None = None
    LIMIT_CONCURRENCY: int | None = None
    LIMIT_MAX_REQUESTS: int | None = None
    CORS_MIDDLEWARE_ALLOW_CREDENTIALS: bool = True
    CORS_MIDDLEWARE_ALLOW_HEADERS: list = ["*"]
    CORS_MIDDLEWARE_ALLOW_METHODS: list = ["*"]
    CORS_MIDDLEWARE_ALLOW_ORIGINS: list = ["*"]
    PROXY_HEADERS: bool = True
    RELOAD: bool = False
    SERVER_HEADER: bool = True
    SERVE_HOST: str = "0.0.0.0"
    SERVE_PORT: int = 8100
    TIMEOUT_GRACEFUL_SHUTDOWN: int | None = None
    TIMEOUT_KEEP_ALIVE: int = 5
    WORKERS_COUNT: int = 4
    WS_MAX_SIZE: int = 16777216
    WS_PER_MESSAGE_DEFLATE: bool = True
    WS_PING_INTERVAL: float = 20.0
    WS_PING_TIMEOUT: float = 20.0
    OPENAPI_URL: str | None = "/openapi.json"
    DOCS_URL: str | None = None
    RE_DOCS_URL: str | None = None
    SWAGGER_UI_PARAMS: dict[str, str] | None = {"docExpansion": "none"}


class GrpcConfig(BaseModel):
    SERVE_PORT: int = 8100
    SERVE_HOST: str = "[::]"
    THREAD_WORKER_COUNT: int | None = None
    THREAD_PER_CPU_CORE: int = 40  # Adjust based on thread block to cpu time ratio
    SERVER_OPTIONS_CONFIG_LIST: list[tuple[str, int]] = [
        ("grpc.max_metadata_size", 1 * 1024 * 1024),
        ("grpc.max_message_length", 128 * 1024 * 1024),
        ("grpc.max_receive_message_length", 128 * 1024 * 1024),
        ("grpc.max_send_message_length", 128 * 1024 * 1024),
        ("grpc.keepalive_time_ms", 5000),
        ("grpc.keepalive_timeout_ms", 1000),
        ("grpc.http2.min_ping_interval_without_data_ms", 5000),
        ("grpc.max_connection_idle_ms", 10000),
        ("grpc.max_connection_age_ms", 30000),
        ("grpc.max_connection_age_grace_ms", 5000),
        ("grpc.http2.max_pings_without_data", 0),
        ("grpc.keepalive_permit_without_calls", 1),
        ("grpc.http2.max_ping_strikes", 0),
        ("grpc.http2.min_recv_ping_interval_without_data_ms", 4000),
    ]

    STUB_OPTIONS_CONFIG_LIST: list[tuple[str, int | str]] = [
        ("grpc.max_metadata_size", 1 * 1024 * 1024),
        ("grpc.max_message_length", 128 * 1024 * 1024),
        ("grpc.max_receive_message_length", 128 * 1024 * 1024),
        ("grpc.max_send_message_length", 128 * 1024 * 1024),
        ("grpc.keepalive_time_ms", 5000),
        ("grpc.keepalive_timeout_ms", 1000),
        ("grpc.http2.max_pings_without_data", 0),
        ("grpc.keepalive_permit_without_calls", 1),
        (
            "grpc.service_config",
            '{"methodConfig": [{"name": [],'
            ' "timeout": "1s", "waitForReady": true,'
            ' "retryPolicy": {"maxAttempts": 5,'
            ' "initialBackoff": "0.1s",'
            ' "maxBackoff": "1s",'
            ' "backoffMultiplier": 2,'
            ' "retryableStatusCodes": ["UNAVAILABLE", "ABORTED",'
            ' "RESOURCE_EXHAUSTED"]}}]}',
        ),
    ]


class KafkaConfig(BaseModel):
    ACKNOWLEDGE_COUNT: int = 1
    AUTO_OFFSET_RESET: str = "earliest"
    BROKERS_LIST: list = ["localhost:9092"]
    CERT_PEM: str | None = None
    ENABLE_AUTO_COMMIT: bool = False
    MAX_BUFFER_MS: int = 1
    MAX_BUFFER_SIZE: int = 1000
    PASSWORD: str | None = None
    SASL_MECHANISMS: str = "SCRAM-SHA-512"
    SECURITY_PROTOCOL: str = "SASL_SSL"
    SESSION_TIMEOUT_MS: int = 6000
    REQUEST_ACK_TIMEOUT_MS: int = 2000
    DELIVERY_MESSAGE_TIMEOUT_MS: int = 2300
    USER_NAME: str | None = None
    LIST_TOPICS_TIMEOUT: int = 1
    #     use in mock
    TOPIC_MAXIMUM_MESSAGE_COUNT: int = 1000


class KeycloakConfig(BaseModel):
    SERVER_URL: str | None = None
    CLIENT_NAME: str | None = None
    REALM_NAME: str = "services"
    CLIENT_SECRET_KEY: str | None = None
    DATA_REFRESH_INTERVAL: int = 5
    LRU_CACHE_MAX_SIZE: int = 100
    ENABLE_SECURE_CONNECTION: bool = True


class SqlAlchemyConfig(BaseModel):
    DATABASE: str | None = None
    DRIVER_NAME: str = "postgresql+psycopg"
    ECHO: bool = False
    ECHO_POOL: bool = False
    ENABLE_FROM_LINTING: bool = True
    HIDE_PARAMETERS: bool = False
    HOST: str | None = None
    ISOLATION_LEVEL: str | None = "REPEATABLE READ"
    PASSWORD: str | None = None
    POOL_MAX_OVERFLOW: int = 1
    POOL_PRE_PING: bool = True
    POOL_RECYCLE_SECONDS: int = 10 * 60
    POOL_RESET_ON_RETURN: str = "rollback"
    POOL_SIZE: int = 20
    POOL_TIMEOUT: int = 30
    POOL_USE_LIFO: bool = True
    PORT: int | None = 5432
    QUERY_CACHE_SIZE: int = 500
    USERNAME: str | None = None


class PrometheusConfig(BaseModel):
    IS_ENABLED: bool = False
    SERVER_PORT: int = 8200


class RedisConfig(BaseModel):
    MASTER_HOST: str | None = None
    SLAVE_HOST: str | None = None
    PORT: int = 6379
    DATABASE: int = 0
    PASSWORD: str | None = None
    DECODE_RESPONSES: Literal[True] = True
    VERSION: int = 7
    HEALTH_CHECK_INTERVAL: int = 10


class SentryConfig(BaseModel):
    IS_ENABLED: bool = False
    DSN: str | None = None
    DEBUG: bool = False
    RELEASE: str = ""
    SAMPLE_RATE: float = 1.0  # between zero and one
    TRACES_SAMPLE_RATE: float = 0.0  # between zero and one


class KavenegarConfig(BaseModel):
    SERVER_URL: str | None = None
    API_KEY: str | None = None
    PHONE_NUMBER: str | None = None


class AuthConfig(BaseModel):
    # JWT Settings
    SECRET_KEY: SecretStr | None = None
    ACCESS_TOKEN_EXPIRES_IN: int = 1 * 60 * 60  # 1 hour in seconds
    REFRESH_TOKEN_EXPIRES_IN: int = 24 * 60 * 60  # 24 hours in seconds
    HASH_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = "your-app-name"
    JWT_AUDIENCE: str = "your-app-audience"
    TOKEN_VERSION: int = 1

    # TOTP Settings
    TOTP_SECRET_KEY: SecretStr | None = None
    TOTP_LENGTH: int = Field(default=6, ge=6, le=8)
    TOTP_EXPIRES_IN: int = Field(default=300, description="TOTP expiration time in seconds (5 minutes)")
    TOTP_TIME_STEP: int = Field(default=30, description="TOTP time step in seconds")
    TOTP_VERIFICATION_WINDOW: int = Field(default=1, description="Number of time steps to check before/after")
    TOTP_MAX_ATTEMPTS: int = Field(default=3, description="Maximum failed TOTP attempts before lockout")
    TOTP_LOCKOUT_TIME: int = Field(default=300, description="Lockout time in seconds after max attempts")

    # Rate Limiting Settings
    LOGIN_RATE_LIMIT: int = Field(default=5, description="Maximum login attempts per minute")
    TOTP_RATE_LIMIT: int = Field(default=3, description="Maximum TOTP requests per minute")
    PASSWORD_RESET_RATE_LIMIT: int = Field(default=3, description="Maximum password reset requests per hour")

    # Password Policy
    HASH_ITERATIONS: int = 100000
    MIN_LENGTH: int = Field(default=12, ge=8)
    REQUIRE_DIGIT: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_SPECIAL: bool = True
    REQUIRE_UPPERCASE: bool = True
    SALT_LENGTH: int = 16
    SPECIAL_CHARACTERS: set[str] = Field(default=set("!@#$%^&*()-_+="), description="Set of allowed special characters")
    PASSWORD_HISTORY_SIZE: int = Field(default=3, description="Number of previous passwords to remember")

    # Token Security
    ENABLE_JTI_CLAIM: bool = Field(default=True, description="Enable JWT ID claim for token tracking")
    ENABLE_TOKEN_ROTATION: bool = Field(default=True, description="Enable refresh token rotation")
    REFRESH_TOKEN_REUSE_INTERVAL: int = Field(default=60, description="Grace period for refresh token reuse in seconds")


class EmailConfig(BaseModel):
    SMTP_SERVER: str | None = None
    SMTP_PORT: int = 587
    USERNAME: str | None = None
    PASSWORD: str | None = None
    POOL_SIZE: int = 5
    CONNECTION_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    ATTACHMENT_MAX_SIZE: int = 5 * 1024 * 1024


class FileConfig(BaseModel):
    SECRET_KEY: str | None = Field(default=None, description="Secret key used for generating secure file links")
    DEFAULT_EXPIRY_MINUTES: int = Field(
        default=60,
        ge=1,
        description="Default number of minutes until link expiration",  # Default 60 minutes (1 hour)
    )
    ALLOWED_EXTENSIONS: list[str] = Field(default=["jpg", "jpeg", "png"], description="List of allowed file extensions")


class DatetimeConfig(BaseModel):
    TIME_IR_API_KEY: str | None = "ZAVdqwuySASubByCed5KYuYMzb9uB2f7"
    TIME_IR_API_ENDPOINT: str | None = "https://api.time.ir/v1/event/fa/events/calendar"
    REQUEST_TIMEOUT: int = 5
    MAX_RETRIES: int = 3
    CACHE_TTL: int = 86400  # TTL for cache in seconds (24 hours)

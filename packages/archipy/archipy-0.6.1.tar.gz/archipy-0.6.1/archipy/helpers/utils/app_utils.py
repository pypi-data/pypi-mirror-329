import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from archipy.configs.base_config import BaseConfig
from archipy.helpers.utils.base_utils import BaseUtils
from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors import (
    BaseError,
    InvalidArgumentError,
    UnavailableError,
    UnknownError,
)


class FastAPIExceptionHandler:
    """Handles various types of errors and converts them to appropriate JSON responses."""

    @staticmethod
    def create_error_response(exception: BaseError) -> JSONResponse:
        """Creates a standardized error response.

        Args:
            exception (BaseError): The exception to be converted into a response.

        Returns:
            JSONResponse: A JSON response containing the exception details.
        """
        BaseUtils.capture_exception(exception)
        return JSONResponse(status_code=exception.http_status_code, content=exception.to_dict())

    @staticmethod
    async def custom_exception_handler(request: Request, exception: BaseError) -> JSONResponse:
        """Handles custom errors.

        Args:
            request (Request): The incoming request.
            exception (BaseError): The custom exception to handle.

        Returns:
            JSONResponse: A JSON response containing the exception details.
        """
        return FastAPIExceptionHandler.create_error_response(exception)

    # TODO Remove http_exception_handler
    @staticmethod
    async def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
        """Handles HTTP errors.

        Args:
            request (Request): The incoming request.
            exception (HTTPException): The HTTP exception to handle.

        Returns:
            JSONResponse: A JSON response containing the exception details.
        """
        detail = ErrorDetailDTO(
            code="TODO_REMOVE_ME",
            http_status=exception.status_code,
            message_en=exception.detail,
            message_fa=exception.detail,
        )
        exception = BaseError(detail, lang="en")
        return FastAPIExceptionHandler.create_error_response(exception)

    @staticmethod
    async def generic_exception_handler(request: Request, exception: Exception) -> JSONResponse:
        """Handles generic errors.

        Args:
            request (Request): The incoming request.
            exception (Exception): The generic exception to handle.

        Returns:
            JSONResponse: A JSON response containing the exception details.
        """
        return FastAPIExceptionHandler.create_error_response(UnknownError())

    @staticmethod
    async def validation_exception_handler(request: Request, exception: ValidationError) -> JSONResponse:
        """Handles validation errors.

        Args:
            request (Request): The incoming request.
            exception (ValidationError): The validation exception to handle.

        Returns:
            JSONResponse: A JSON response containing the validation error details.
        """
        errors = []
        for error in exception.errors():
            errors.append(
                {
                    "field": ".".join(str(x) for x in error["loc"]),
                    "message": error["msg"],
                    "value": str(error.get("input", "")),
                },
            )

        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content={"error": "VALIDATION_ERROR", "detail": errors},
        )


class FastAPIUtils:
    """Utility class for FastAPI configuration and setup."""

    @staticmethod
    def custom_generate_unique_id(route: APIRoute) -> str:
        """Generates a unique ID for API routes.

        Args:
            route (APIRoute): The route for which to generate a unique ID.

        Returns:
            str: A unique ID for the route.
        """
        return f"{route.tags[0]}-{route.name}" if route.tags else route.name

    @staticmethod
    def setup_sentry(config: BaseConfig) -> None:
        """Initializes Sentry configuration if enabled.

        Args:
            config (BaseConfig): The configuration object containing Sentry settings.
        """
        if not config.SENTRY.IS_ENABLED:
            return

        try:
            import sentry_sdk

            sentry_sdk.init(
                dsn=config.SENTRY.DSN,
                debug=config.SENTRY.DEBUG,
                release=config.SENTRY.RELEASE,
                sample_rate=config.SENTRY.SAMPLE_RATE,
                traces_sample_rate=config.SENTRY.TRACES_SAMPLE_RATE,
                environment=config.ENVIRONMENT,
            )
        except Exception as e:
            logging.exception(f"Failed to initialize Sentry: {e}")

    @staticmethod
    def setup_cors(app: FastAPI, config: BaseConfig) -> None:
        """Configures CORS middleware.

        Args:
            app (FastAPI): The FastAPI application instance.
            config (BaseConfig): The configuration object containing CORS settings.
        """
        origins = [str(origin).strip("/") for origin in config.FASTAPI.CORS_MIDDLEWARE_ALLOW_ORIGINS]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=config.FASTAPI.CORS_MIDDLEWARE_ALLOW_CREDENTIALS,
            allow_methods=config.FASTAPI.CORS_MIDDLEWARE_ALLOW_METHODS,
            allow_headers=config.FASTAPI.CORS_MIDDLEWARE_ALLOW_HEADERS,
        )

    @staticmethod
    def setup_elastic_apm(app: FastAPI, config: BaseConfig) -> None:
        """Configures Elastic APM if enabled.

        Args:
            app (FastAPI): The FastAPI application instance.
            config (BaseConfig): The configuration object containing Elastic APM settings.
        """
        if not config.ELASTIC_APM.IS_ENABLED:
            return

        try:
            import elasticapm
            from elasticapm.contrib.starlette import ElasticAPM

            apm_client = elasticapm.get_client()
            app.add_middleware(ElasticAPM, client=apm_client)
        except Exception as e:
            logging.exception(f"Failed to initialize Elastic APM: {e}")

    @staticmethod
    def setup_exception_handlers(app: FastAPI) -> None:
        """Configures exception handlers for the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        app.add_exception_handler(RequestValidationError, FastAPIExceptionHandler.validation_exception_handler)
        app.add_exception_handler(ValidationError, FastAPIExceptionHandler.validation_exception_handler)
        app.add_exception_handler(BaseError, FastAPIExceptionHandler.custom_exception_handler)
        app.add_exception_handler(HTTPException, FastAPIExceptionHandler.http_exception_handler)
        app.add_exception_handler(Exception, FastAPIExceptionHandler.generic_exception_handler)


class AppUtils:
    """Utility class for creating and configuring FastAPI applications."""

    @classmethod
    def create_fastapi_app(cls, config: BaseConfig | None = None, configure_exception_handlers: bool = True) -> FastAPI:
        """Creates and configures a FastAPI application.

        Args:
            config (BaseConfig | None): Optional custom configuration. If not provided, uses global config.
            configure_exception_handlers (bool): Whether to configure exception handlers.

        Returns:
            FastAPI: The configured FastAPI application instance.
        """
        config = config or BaseConfig.global_config()

        # Define common responses for all endpoints
        common_responses = BaseUtils.get_fastapi_exception_responses(
            [UnknownError, UnavailableError, InvalidArgumentError],
        )
        app = FastAPI(
            title=config.FASTAPI.PROJECT_NAME,
            openapi_url=config.FASTAPI.OPENAPI_URL,
            generate_unique_id_function=FastAPIUtils.custom_generate_unique_id,
            swagger_ui_parameters=config.FASTAPI.SWAGGER_UI_PARAMS,
            docs_url=config.FASTAPI.DOCS_URL,
            redocs_url=config.FASTAPI.RE_DOCS_URL,
            responses=common_responses,
        )

        FastAPIUtils.setup_sentry(config)
        FastAPIUtils.setup_cors(app, config)
        FastAPIUtils.setup_elastic_apm(app, config)

        if configure_exception_handlers:
            FastAPIUtils.setup_exception_handlers(app)

        return app

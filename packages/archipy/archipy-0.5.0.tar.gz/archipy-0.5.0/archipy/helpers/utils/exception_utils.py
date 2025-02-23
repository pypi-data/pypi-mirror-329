import logging
from typing import Any

from archipy.configs.base_config import BaseConfig
from archipy.models.dtos.fastapi_exception_response_dto import (
    FastAPIExceptionResponseDTO,
    ValidationExceptionResponseDTO,
)
from archipy.models.exceptions import CommonsBaseException

try:
    from http import HTTPStatus

    from fastapi import Request
    from fastapi.responses import JSONResponse

    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False
    HTTPStatus = None

try:
    from grpc import StatusCode

    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    StatusCode = None


class ExceptionUtils:
    """A utility class for handling exceptions, including capturing, reporting, and generating responses."""

    @staticmethod
    def capture_exception(exception: BaseException) -> None:
        """Captures an exception and reports it to configured external services.

        This method logs the exception locally and optionally reports it to Sentry and Elastic APM,
        depending on the configuration.

        Args:
            exception (BaseException): The exception to capture and report.
        """
        # Always log the exception locally
        logging.exception("An exception occurred: %s", str(exception))
        config = BaseConfig.global_config()

        # Report exception to Sentry if enabled
        if config.SENTRY.IS_ENABLED:
            try:
                import sentry_sdk

                sentry_sdk.capture_exception(exception)
            except ImportError:
                logging.error("sentry_sdk is not installed, cannot capture exception in Sentry.")

        # Report exception to Elastic APM if enabled
        if config.ELASTIC_APM.IS_ENABLED:
            try:
                import elasticapm

                client = elasticapm.get_client()
                client.capture_exception()
            except ImportError:
                logging.error("elasticapm is not installed, cannot capture exception in Elastic APM.")

    @staticmethod
    async def async_handle_fastapi_exception(request: Request, exception: CommonsBaseException) -> JSONResponse:
        """Handles a FastAPI exception and returns a JSON response.

        Args:
            request (Request): The incoming FastAPI request.
            exception (CommonsBaseException): The exception to handle.

        Returns:
            JSONResponse: A JSON response containing the exception details.

        Raises:
            NotImplementedError: If FastAPI is not available.
        """
        if not HTTP_AVAILABLE:
            raise NotImplementedError
        return JSONResponse(
            status_code=exception.http_status_code or HTTPStatus.INTERNAL_SERVER_ERROR,
            content=exception.to_dict(),
        )

    @staticmethod
    def handle_grpc_exception(exception: CommonsBaseException) -> tuple[int, str]:
        """Handles a gRPC exception and returns a tuple of status code and message.

        Args:
            exception (CommonsBaseException): The exception to handle.

        Returns:
            tuple[int, str]: A tuple containing the gRPC status code and error message.

        Raises:
            NotImplementedError: If gRPC is not available.
        """
        if not GRPC_AVAILABLE:
            raise NotImplementedError
        return (exception.grpc_status_code or StatusCode.UNKNOWN.value[0], exception.get_message())

    @staticmethod
    def get_fastapi_exception_responses(exceptions: list[type[CommonsBaseException]]) -> dict[int, dict[str, Any]]:
        """Generates OpenAPI response documentation for the given exceptions.

        This method creates OpenAPI-compatible response schemas for FastAPI exceptions,
        including validation errors and custom exceptions.

        Args:
            exceptions (list[type[CommonsBaseException]]): A list of exception types to generate responses for.

        Returns:
            dict[int, dict[str, Any]]: A dictionary mapping HTTP status codes to their corresponding response schemas.
        """
        responses = {}

        # Add validation error response by default
        validation_response = ValidationExceptionResponseDTO()
        responses[validation_response.status_code] = validation_response.model

        exception_schemas = {
            "InvalidPhoneNumberException": {
                "phone_number": {"type": "string", "example": "1234567890", "description": "The invalid phone number"},
            },
            "InvalidLandlineNumberException": {
                "landline_number": {
                    "type": "string",
                    "example": "02112345678",
                    "description": "The invalid landline number",
                },
            },
            "NotFoundException": {
                "resource_type": {
                    "type": "string",
                    "example": "user",
                    "description": "Type of resource that was not found",
                },
            },
            "InvalidNationalCodeException": {
                "national_code": {
                    "type": "string",
                    "example": "1234567890",
                    "description": "The invalid national code",
                },
            },
            "InvalidArgumentException": {
                "argument": {
                    "type": "string",
                    "example": "mobile_number",
                    "description": "Argument that was invalid",
                },
            },
        }

        for exc in exceptions:
            error = exc().error_detail
            if error.http_status:
                additional_properties = exception_schemas.get(exc.__name__)
                response = FastAPIExceptionResponseDTO(error, additional_properties)
                responses[response.status_code] = response.model

        return responses

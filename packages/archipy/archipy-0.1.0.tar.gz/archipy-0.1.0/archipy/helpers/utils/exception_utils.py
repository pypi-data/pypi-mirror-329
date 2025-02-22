import logging
from typing import Any

from archipy.configs.base_config import BaseConfig
from archipy.models.dtos.exception_dto import ExceptionDetailDTO
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
    @staticmethod
    def capture_exception(exception: BaseException) -> None:
        """Capture an exception and report it to configured external services."""
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
    def create_exception_detail(
        code: str,
        message_en: str,
        message_fa: str,
        http_status: int | HTTPStatus | None = None,
        grpc_status: int | StatusCode | None = None,
    ) -> ExceptionDetailDTO:
        """Helper function to create ExceptionDetailDTO with appropriate status codes"""
        status_kwargs = {}

        if HTTP_AVAILABLE and http_status is not None:
            status_kwargs['http_status'] = http_status.value if isinstance(http_status, HTTPStatus) else http_status

        if GRPC_AVAILABLE and grpc_status is not None:
            status_kwargs['grpc_status'] = grpc_status.value[0] if isinstance(grpc_status, StatusCode) else grpc_status

        return ExceptionDetailDTO(code=code, message_en=message_en, message_fa=message_fa, **status_kwargs)

    @staticmethod
    async def async_handle_fastapi_exception(request: Request, exception: CommonsBaseException) -> JSONResponse:
        if not HTTP_AVAILABLE:
            raise NotImplementedError
        return JSONResponse(
            status_code=exception.http_status_code or HTTPStatus.INTERNAL_SERVER_ERROR,
            content=exception.to_dict(),
        )

    @staticmethod
    def handle_grpc_exception(exception: CommonsBaseException) -> tuple[int, str]:
        if not GRPC_AVAILABLE:
            raise NotImplementedError
        return (exception.grpc_status_code or StatusCode.UNKNOWN.value[0], exception.get_message())

    @staticmethod
    def get_fastapi_exception_responses(exceptions: list[type[CommonsBaseException]]) -> dict[int, dict[str, Any]]:
        """Generate OpenAPI response documentation for given exceptions"""
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

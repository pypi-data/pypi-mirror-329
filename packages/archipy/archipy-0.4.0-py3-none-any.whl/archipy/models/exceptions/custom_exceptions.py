from typing import Any

from archipy.models.dtos.exception_dto import ExceptionDetailDTO
from archipy.models.types.exception_message_types import ExceptionMessageType

try:
    from http import HTTPStatus

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


class CommonsBaseException(Exception):
    """Base exception class for all custom exceptions"""

    def __init__(
        self,
        error: ExceptionDetailDTO | ExceptionMessageType | None = None,
        lang: str = "fa",
        additional_data: dict | None = None,
        *args: Any,
    ) -> None:
        """
        Initialize the base exception.

        Args:
            error: The error detail or message. Can be:
                - ErrorDetail: Direct error detail object
                - ExceptionMessageType: Enum member containing error detail
                - None: Will use UNKNOWN_ERROR
            lang: Language code for the error message ("fa" or "en")
            additional_data: Additional context data for the error
            *args: Additional arguments for the base Exception class
        """
        if isinstance(error, ExceptionMessageType):
            self.error_detail = error.value
        elif isinstance(error, ExceptionDetailDTO):
            self.error_detail = error
        else:
            self.error_detail = ExceptionMessageType.UNKNOWN_ERROR.value

        self.lang = lang.lower()
        if self.lang not in ["fa", "en"]:
            self.lang = "fa"

        self.additional_data = additional_data or {}

        # Initialize base Exception with the message
        super().__init__(self.get_message(), *args)

    def get_message(self) -> str:
        """Get the localized error message based on the language setting."""
        return self.error_detail.message_fa if self.lang == "fa" else self.error_detail.message_en

    def to_dict(self) -> dict:
        """
        Convert the exception to a dictionary format for API responses.

        Returns:
            dict: A dictionary containing error details and additional data
        """
        response = {
            "error": self.error_detail.code,
            "detail": self.error_detail.model_dump(mode="json", exclude_none=True),
        }

        # Add additional data if present
        if self.additional_data:
            response["detail"].update(self.additional_data)

        return response

    @property
    def http_status_code(self) -> int | None:
        """
        Get the HTTP status code if HTTP support is available.

        Returns:
            Optional[int]: The HTTP status code or None if HTTP is not available
        """
        return self.error_detail.http_status if HTTP_AVAILABLE else None

    @property
    def grpc_status_code(self) -> int | None:
        """
        Get the gRPC status code if gRPC support is available.

        Returns:
            Optional[int]: The gRPC status code or None if gRPC is not available
        """
        return self.error_detail.grpc_status if GRPC_AVAILABLE else None

    def __str__(self) -> str:
        """
        String representation of the exception.

        Returns:
            str: A formatted string containing the error code and message
        """
        return f"[{self.error_detail.code}] {self.get_message()}"

    def __repr__(self) -> str:
        """
        Detailed string representation of the exception.

        Returns:
            str: A detailed string representation including all error details
        """
        return (
            f"{self.__class__.__name__}("
            f"code='{self.error_detail.code}', "
            f"message='{self.get_message()}', "
            f"http_status={self.http_status_code}, "
            f"grpc_status={self.grpc_status_code}, "
            f"additional_data={self.additional_data}"
            f")"
        )

    @property
    def code(self) -> str:
        """
        Get the error code.

        Returns:
            str: The error code
        """
        return self.error_detail.code

    @property
    def message(self) -> str:
        """
        Get the current language message.

        Returns:
            str: The error message in the current language
        """
        return self.get_message()

    @property
    def message_en(self) -> str:
        """
        Get the English message.

        Returns:
            str: The English error message
        """
        return self.error_detail.message_en

    @property
    def message_fa(self) -> str:
        """
        Get the Persian message.

        Returns:
            str: The Persian error message
        """
        return self.error_detail.message_fa


# Authentication Exceptions
class InvalidPhoneNumberException(CommonsBaseException):
    def __init__(
        self,
        phone_number: str,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_PHONE.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"phone_number": phone_number})


class InvalidLandlineNumberException(CommonsBaseException):
    def __init__(
        self,
        landline_number: str,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_LANDLINE.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"landline_number": landline_number})


class TokenExpiredException(CommonsBaseException):
    def __init__(self, lang: str = "fa", error: ExceptionDetailDTO = ExceptionMessageType.TOKEN_EXPIRED.value) -> None:
        super().__init__(error, lang)


class InvalidTokenException(CommonsBaseException):
    def __init__(self, lang: str = "fa", error: ExceptionDetailDTO = ExceptionMessageType.INVALID_TOKEN.value) -> None:
        super().__init__(error, lang)


class PermissionDeniedException(CommonsBaseException):
    def __init__(
        self,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.PERMISSION_DENIED.value,
    ) -> None:
        super().__init__(error, lang)


# Resource Exceptions
class NotFoundException(CommonsBaseException):
    def __init__(
        self,
        resource_type: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.NOT_FOUND.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"resource_type": resource_type} if resource_type else None)


class AlreadyExistsException(CommonsBaseException):
    def __init__(
        self,
        resource_type: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.ALREADY_EXISTS.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"resource_type": resource_type} if resource_type else None)


# Validation Exceptions
class InvalidArgumentException(CommonsBaseException):
    def __init__(
        self,
        argument_name: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_ARGUMENT.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"argument": argument_name} if argument_name else None)


class OutOfRangeException(CommonsBaseException):
    def __init__(
        self,
        field_name: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.OUT_OF_RANGE.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"field": field_name} if field_name else None)


# Operation Exceptions
class DeadlineExceededException(CommonsBaseException):
    def __init__(
        self,
        operation: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.DEADLINE_EXCEEDED.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"operation": operation} if operation else None)


class DeprecationException(CommonsBaseException):

    def __init__(
        self,
        operation: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.DEPRECATION.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"operation": operation} if operation else None)


class FailedPreconditionException(CommonsBaseException):
    def __init__(
        self,
        condition: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.FAILED_PRECONDITION.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"condition": condition} if condition else None)


class ResourceExhaustedException(CommonsBaseException):
    def __init__(
        self,
        resource_type: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.RESOURCE_EXHAUSTED.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"resource_type": resource_type} if resource_type else None)


class AbortedException(CommonsBaseException):
    def __init__(
        self,
        reason: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.ABORTED.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"reason": reason} if reason else None)


class CancelledException(CommonsBaseException):
    def __init__(
        self,
        reason: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.CANCELLED.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"reason": reason} if reason else None)


# System Exceptions
class InternalException(CommonsBaseException):
    def __init__(
        self,
        details: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.INTERNAL_ERROR.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"details": details} if details else None)


class DataLossException(CommonsBaseException):
    def __init__(
        self,
        details: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.DATA_LOSS.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"details": details} if details else None)


class UnImplementedException(CommonsBaseException):
    def __init__(
        self,
        feature: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.UNIMPLEMENTED.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"feature": feature} if feature else None)


class UnavailableException(CommonsBaseException):
    def __init__(
        self,
        service: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.UNAVAILABLE.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"service": service} if service else None)


class UnknownException(CommonsBaseException):
    def __init__(
        self,
        details: str | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.UNKNOWN_ERROR.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"details": details} if details else None)


class InvalidNationalCodeException(CommonsBaseException):
    def __init__(
        self,
        national_code: str,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_NATIONAL_CODE.value,
    ) -> None:
        super().__init__(error, lang, additional_data={"national_code": national_code})


class InvalidEntityTypeException(CommonsBaseException):
    def __init__(
        self,
        entity_type: Any | None = None,
        expected_type: type | None = None,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_ENTITY_TYPE.value,
    ):
        super().__init__(error, lang, additional_data={"entity_type": entity_type, "expected_type": expected_type})


class DeadlockDetectedException(CommonsBaseException):
    def __init__(
        self,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.DEADLOCK_TYPE.value,
    ):
        super().__init__(
            error,
            lang,
        )


class UnauthenticatedException(CommonsBaseException):
    def __init__(
        self,
        lang: str = "fa",
        error: ExceptionDetailDTO = ExceptionMessageType.UNAUTHENTICATED_TYPE.value,
    ):
        super().__init__(error, lang)

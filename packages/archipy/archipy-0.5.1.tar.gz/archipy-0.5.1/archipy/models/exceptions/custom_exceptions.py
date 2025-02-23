from typing import Any

from archipy.models.dtos.exception_dto import ExceptionDetailDTO
from archipy.models.types.exception_message_types import ExceptionMessageType
from archipy.models.types.language_type import LanguageType

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
    """Base exception class for all custom exceptions."""

    def __init__(
        self,
        error: ExceptionDetailDTO | ExceptionMessageType | None = None,
        lang: LanguageType = LanguageType.FA,
        additional_data: dict | None = None,
        *args: Any,
    ) -> None:
        """Initializes the base exception.

        Args:
            error: The error detail or message. Can be:
                - ErrorDetail: Direct error detail object
                - ExceptionMessageType: Enum member containing error detail
                - None: Will use UNKNOWN_ERROR
            lang: Language code for the error message (defaults to Persian).
            additional_data: Additional context data for the error.
            *args: Additional arguments for the base Exception class.
        """
        if isinstance(error, ExceptionMessageType):
            self.error_detail = error.value
        elif isinstance(error, ExceptionDetailDTO):
            self.error_detail = error
        else:
            self.error_detail = ExceptionMessageType.UNKNOWN_ERROR.value

        self.lang = lang
        self.additional_data = additional_data or {}

        # Initialize base Exception with the message
        super().__init__(self.get_message(), *args)

    def get_message(self) -> str:
        """Gets the localized error message based on the language setting.

        Returns:
            str: The error message in the current language.
        """
        return self.error_detail.message_fa if self.lang == LanguageType.FA else self.error_detail.message_en

    def to_dict(self) -> dict:
        """Converts the exception to a dictionary format for API responses.

        Returns:
            dict: A dictionary containing error details and additional data.
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
        """Gets the HTTP status code if HTTP support is available.

        Returns:
            Optional[int]: The HTTP status code or None if HTTP is not available.
        """
        return self.error_detail.http_status if HTTP_AVAILABLE else None

    @property
    def grpc_status_code(self) -> int | None:
        """Gets the gRPC status code if gRPC support is available.

        Returns:
            Optional[int]: The gRPC status code or None if gRPC is not available.
        """
        return self.error_detail.grpc_status if GRPC_AVAILABLE else None

    def __str__(self) -> str:
        """String representation of the exception.

        Returns:
            str: A formatted string containing the error code and message.
        """
        return f"[{self.error_detail.code}] {self.get_message()}"

    def __repr__(self) -> str:
        """Detailed string representation of the exception.

        Returns:
            str: A detailed string representation including all error details.
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
        """Gets the error code.

        Returns:
            str: The error code.
        """
        return self.error_detail.code

    @property
    def message(self) -> str:
        """Gets the current language message.

        Returns:
            str: The error message in the current language.
        """
        return self.get_message()

    @property
    def message_en(self) -> str:
        """Gets the English message.

        Returns:
            str: The English error message.
        """
        return self.error_detail.message_en

    @property
    def message_fa(self) -> str:
        """Gets the Persian message.

        Returns:
            str: The Persian error message.
        """
        return self.error_detail.message_fa


# Authentication Exceptions
class InvalidPhoneNumberException(CommonsBaseException):
    """Exception raised for invalid phone numbers."""

    def __init__(
        self,
        phone_number: str,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_PHONE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            phone_number: The invalid phone number.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"phone_number": phone_number})


class InvalidLandlineNumberException(CommonsBaseException):
    """Exception raised for invalid landline numbers."""

    def __init__(
        self,
        landline_number: str,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_LANDLINE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            landline_number: The invalid landline number.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"landline_number": landline_number})


class TokenExpiredException(CommonsBaseException):
    """Exception raised when a token has expired."""

    def __init__(
        self,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.TOKEN_EXPIRED.value,
    ) -> None:
        """Initializes the exception.

        Args:
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang)


class InvalidTokenException(CommonsBaseException):
    """Exception raised when a token is invalid."""

    def __init__(
        self,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_TOKEN.value,
    ) -> None:
        """Initializes the exception.

        Args:
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang)


class PermissionDeniedException(CommonsBaseException):
    """Exception raised when permission is denied."""

    def __init__(
        self,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.PERMISSION_DENIED.value,
    ) -> None:
        """Initializes the exception.

        Args:
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang)


# Resource Exceptions
class NotFoundException(CommonsBaseException):
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        resource_type: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.NOT_FOUND.value,
    ) -> None:
        """Initializes the exception.

        Args:
            resource_type: The type of resource that was not found.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"resource_type": resource_type} if resource_type else None)


class AlreadyExistsException(CommonsBaseException):
    """Exception raised when a resource already exists."""

    def __init__(
        self,
        resource_type: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.ALREADY_EXISTS.value,
    ) -> None:
        """Initializes the exception.

        Args:
            resource_type: The type of resource that already exists.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"resource_type": resource_type} if resource_type else None)


# Validation Exceptions
class InvalidArgumentException(CommonsBaseException):
    """Exception raised for invalid arguments."""

    def __init__(
        self,
        argument_name: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_ARGUMENT.value,
    ) -> None:
        """Initializes the exception.

        Args:
            argument_name: The name of the invalid argument.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"argument": argument_name} if argument_name else None)


class OutOfRangeException(CommonsBaseException):
    """Exception raised when a value is out of range."""

    def __init__(
        self,
        field_name: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.OUT_OF_RANGE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            field_name: The name of the field that is out of range.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"field": field_name} if field_name else None)


# Operation Exceptions
class DeadlineExceededException(CommonsBaseException):
    """Exception raised when a deadline is exceeded."""

    def __init__(
        self,
        operation: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.DEADLINE_EXCEEDED.value,
    ) -> None:
        """Initializes the exception.

        Args:
            operation: The operation that exceeded the deadline.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"operation": operation} if operation else None)


class DeprecationException(CommonsBaseException):
    """Exception raised for deprecated operations."""

    def __init__(
        self,
        operation: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.DEPRECATION.value,
    ) -> None:
        """Initializes the exception.

        Args:
            operation: The deprecated operation.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"operation": operation} if operation else None)


class FailedPreconditionException(CommonsBaseException):
    """Exception raised when a precondition fails."""

    def __init__(
        self,
        condition: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.FAILED_PRECONDITION.value,
    ) -> None:
        """Initializes the exception.

        Args:
            condition: The failed precondition.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"condition": condition} if condition else None)


class ResourceExhaustedException(CommonsBaseException):
    """Exception raised when resources are exhausted."""

    def __init__(
        self,
        resource_type: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.RESOURCE_EXHAUSTED.value,
    ) -> None:
        """Initializes the exception.

        Args:
            resource_type: The type of resource that is exhausted.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"resource_type": resource_type} if resource_type else None)


class AbortedException(CommonsBaseException):
    """Exception raised when an operation is aborted."""

    def __init__(
        self,
        reason: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.ABORTED.value,
    ) -> None:
        """Initializes the exception.

        Args:
            reason: The reason for the abort.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"reason": reason} if reason else None)


class CancelledException(CommonsBaseException):
    """Exception raised when an operation is cancelled."""

    def __init__(
        self,
        reason: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.CANCELLED.value,
    ) -> None:
        """Initializes the exception.

        Args:
            reason: The reason for the cancellation.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"reason": reason} if reason else None)


# System Exceptions
class InternalException(CommonsBaseException):
    """Exception raised for internal errors."""

    def __init__(
        self,
        details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.INTERNAL_ERROR.value,
    ) -> None:
        """Initializes the exception.

        Args:
            details: Additional details about the internal error.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"details": details} if details else None)


class DataLossException(CommonsBaseException):
    """Exception raised when data is lost."""

    def __init__(
        self,
        details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.DATA_LOSS.value,
    ) -> None:
        """Initializes the exception.

        Args:
            details: Additional details about the data loss.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"details": details} if details else None)


class UnImplementedException(CommonsBaseException):
    """Exception raised for unimplemented features."""

    def __init__(
        self,
        feature: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.UNIMPLEMENTED.value,
    ) -> None:
        """Initializes the exception.

        Args:
            feature: The unimplemented feature.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"feature": feature} if feature else None)


class UnavailableException(CommonsBaseException):
    """Exception raised when a service is unavailable."""

    def __init__(
        self,
        service: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.UNAVAILABLE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            service: The unavailable service.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"service": service} if service else None)


class UnknownException(CommonsBaseException):
    """Exception raised for unknown errors."""

    def __init__(
        self,
        details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.UNKNOWN_ERROR.value,
    ) -> None:
        """Initializes the exception.

        Args:
            details: Additional details about the unknown error.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"details": details} if details else None)


class InvalidNationalCodeException(CommonsBaseException):
    """Exception raised for invalid national codes."""

    def __init__(
        self,
        national_code: str,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_NATIONAL_CODE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            national_code: The invalid national code.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"national_code": national_code})


class InvalidEntityTypeException(CommonsBaseException):
    """Exception raised for invalid entity types."""

    def __init__(
        self,
        entity_type: Any | None = None,
        expected_type: type | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.INVALID_ENTITY_TYPE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            entity_type: The invalid entity type.
            expected_type: The expected entity type.
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang, additional_data={"entity_type": entity_type, "expected_type": expected_type})


class DeadlockDetectedException(CommonsBaseException):
    """Exception raised when a deadlock is detected."""

    def __init__(
        self,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.DEADLOCK_TYPE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang)


class UnauthenticatedException(CommonsBaseException):
    """Exception raised when a user is unauthenticated."""

    def __init__(
        self,
        lang: LanguageType = LanguageType.FA,
        error: ExceptionDetailDTO = ExceptionMessageType.UNAUTHENTICATED_TYPE.value,
    ) -> None:
        """Initializes the exception.

        Args:
            lang: Language code for the error message (defaults to Persian).
            error: The error detail or message.
        """
        super().__init__(error, lang)

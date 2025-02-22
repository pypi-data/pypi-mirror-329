from archipy.models.dtos import BaseDTO


class ExceptionDetailDTO(BaseDTO):
    """Standardized error detail model"""

    code: str
    message_en: str
    message_fa: str
    http_status: int | None = None
    grpc_status: int | None = None

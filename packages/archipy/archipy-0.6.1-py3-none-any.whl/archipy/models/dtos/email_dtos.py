import mimetypes
from typing import BinaryIO, Self

from pydantic import Field, field_validator, model_validator

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.types.email_types import EmailAttachmentDispositionType, EmailAttachmentType


class EmailAttachmentDTO(BaseDTO):
    """Pydantic model for email attachments"""

    content: str | bytes | BinaryIO
    filename: str
    content_type: str | None = Field(default=None)
    content_disposition: EmailAttachmentDispositionType = Field(default=EmailAttachmentDispositionType.ATTACHMENT)
    content_id: str | None = Field(default=None)
    attachment_type: EmailAttachmentType
    max_size: int

    @field_validator("content_type")
    def set_content_type(cls, v, values):
        if v is None and "filename" in values:
            content_type, _ = mimetypes.guess_type(values["filename"])
            return content_type or "application/octet-stream"
        return v

    @model_validator(mode="after")
    def validate_pagination(cls, model: Self) -> Self:
        content = model.content
        if isinstance(content, (str, bytes)):
            content_size = len(content)
            if content_size > model.max_size:
                raise ValueError(f"Attachment size exceeds maximum allowed size of {model.max_size} bytes")
        return model

    @field_validator("content_id")
    def validate_content_id(cls, v, values):
        if v and not v.startswith("<"):
            return f"<{v}>"
        return v

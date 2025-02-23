from enum import StrEnum


class EmailAttachmentType(StrEnum):
    """Enum for different types of attachments"""

    FILE = "file"
    BASE64 = "base64"
    URL = "url"
    BINARY = "binary"


class EmailAttachmentDispositionType(StrEnum):
    """Enum for attachment disposition types"""

    ATTACHMENT = "attachment"
    INLINE = "inline"

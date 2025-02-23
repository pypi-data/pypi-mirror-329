from abc import abstractmethod

from pydantic import EmailStr

from archipy.models.dtos.email_dtos import EmailAttachmentDTO


class EmailPort:
    @abstractmethod
    def send_email(
        self,
        to_email: EmailStr | list[EmailStr],
        subject: str,
        body: str,
        cc: EmailStr | list[EmailStr] | None = None,
        bcc: EmailStr | list[EmailStr] | None = None,
        attachments: list[str | EmailAttachmentDTO] | None = None,
        html: bool = False,
        template: str | None = None,
        template_vars: dict | None = None,
    ) -> None:
        raise NotImplementedError

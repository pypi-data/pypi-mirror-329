import base64
import hashlib
import os

from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import FileConfig
from archipy.helpers.utils.datetime_utils import DatetimeUtils


class FileUtils:

    @staticmethod
    def _create_secure_link_hash(path: str, expires_at: float, file_config: FileConfig | None = None) -> str:
        configs: FileConfig = file_config or BaseConfig.global_config().FILE  # type: ignore [attr-defined]
        secret: str | None = configs.SECRET_KEY
        if secret is None:
            raise ValueError("'SECRET_KEY' cannot be None")
        _input = f"{expires_at}{path} {secret}"
        hash_object = hashlib.md5(_input.encode("utf8"))
        return base64.urlsafe_b64encode(hash_object.digest()).decode("utf-8").rstrip("=")

    @classmethod
    def create_secure_link(
        cls,
        path: str,
        minutes: int | None = None,
        file_config: FileConfig | None = None,
    ) -> str:
        """
        Create a secure link with expiration for file access.

        Args:
            path: The file path to create a secure link for.
            minutes: Number of minutes until link expiration (defaults to config's DEFAULT_EXPIRY_MINUTES).
            file_config: Optional file configuration object.

        Returns:
            str: Secure link with hash and expiration timestamp.

        Raises:
            ValueError: If path is empty or minutes is negative.
        """
        if not path:
            raise ValueError("Path cannot be empty")

        configs: FileConfig = file_config or BaseConfig.global_config().FILE  # type: ignore [attr-defined]
        expiry_minutes: int = minutes if minutes is not None else configs.DEFAULT_EXPIRY_MINUTES

        if expiry_minutes < 1:
            raise ValueError("Minutes must be greater than or equal to 1")

        expires_at = int(DatetimeUtils.get_datetime_after_given_datetime_or_now(minutes=expiry_minutes).timestamp())
        secure_link_hash = cls._create_secure_link_hash(path, expires_at, file_config)

        return f"{path}?md5={secure_link_hash}&expires_at={expires_at}"

    @classmethod
    def validate_file_name(
        cls,
        file_name: str,
        file_config: FileConfig | None = None,
    ) -> bool:
        configs: FileConfig = file_config or BaseConfig.global_config().FILE  # type: ignore [attr-defined]
        allowed_extensions: list[str] = configs.ALLOWED_EXTENSIONS

        if not isinstance(file_name, str):
            raise ValueError(
                "Invalid input: 'name' must be a string ",
            )
        if not allowed_extensions:
            raise ValueError("Invalid input: 'allowed_extensions' must be a list")

        _, ext = os.path.splitext(file_name)
        ext = ext[1:].lower()
        return ext in allowed_extensions and bool(ext)

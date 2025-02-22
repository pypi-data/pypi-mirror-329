from typing import Any
from uuid import UUID, uuid4

from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import AuthConfig
from archipy.helpers.utils.datetime_utils import DatetimeUtils
from archipy.models.exceptions import InvalidTokenException, TokenExpiredException


class JWTUtils:
    """Utility class for JWT token operations with enhanced security and datetime handling."""

    @classmethod
    def create_token(
        cls,
        data: dict[str, Any],
        expires_in: int,
        additional_claims: dict[str, Any] | None = None,
        auth_config: AuthConfig | None = None,
    ) -> str:
        """
        Create a JWT token with enhanced security features.

        Args:
            data: Base claims data
            expires_in: Token expiration time in seconds
            additional_claims: Optional additional claims
            auth_config: Optional auth configuration override

        Returns:
            str: Encoded JWT token

        Raises:
            ValueError: If data is empty or expiration is invalid
        """
        import jwt

        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config
        current_time = DatetimeUtils.get_datetime_utc_now()

        if not data:
            raise ValueError("Token data cannot be empty")
        if expires_in <= 0:
            raise ValueError("Token expiration must be positive")

        to_encode = data.copy()
        expire = DatetimeUtils.get_datetime_after_given_datetime_or_now(seconds=expires_in, datetime_given=current_time)

        # Add standard claims
        to_encode.update(
            {
                # Registered claims (RFC 7519)
                "iss": configs.JWT_ISSUER,
                "aud": configs.JWT_AUDIENCE,
                "exp": expire,
                "iat": current_time,
                "nbf": current_time,
            },
        )

        # Add JWT ID if enabled
        if configs.ENABLE_JTI_CLAIM:
            to_encode["jti"] = str(uuid4())

        # Add additional claims
        if additional_claims:
            to_encode.update(additional_claims)

        return jwt.encode(to_encode, configs.SECRET_KEY.get_secret_value(), algorithm=configs.HASH_ALGORITHM)

    @classmethod
    def create_access_token(
        cls,
        user_uuid: UUID,
        additional_claims: dict[str, Any] | None = None,
        auth_config: AuthConfig | None = None,
    ) -> str:
        """
        Create an access token for a user.

        Args:
            user_uuid: User's UUID
            additional_claims: Optional additional claims
            auth_config: Optional auth configuration override

        Returns:
            str: Encoded access token
        """
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config

        return cls.create_token(
            data={
                "sub": str(user_uuid),
                "type": "access",
                "token_version": configs.TOKEN_VERSION,
            },
            expires_in=configs.ACCESS_TOKEN_EXPIRES_IN,
            additional_claims=additional_claims,
            auth_config=configs,
        )

    @classmethod
    def create_refresh_token(
        cls,
        user_uuid: UUID,
        additional_claims: dict[str, Any] | None = None,
        auth_config: AuthConfig | None = None,
    ) -> str:
        """
        Create a refresh token for a user.

        Args:
            user_uuid: User's UUID
            additional_claims: Optional additional claims
            auth_config: Optional auth configuration override

        Returns:
            str: Encoded refresh token
        """
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config

        return cls.create_token(
            data={
                "sub": str(user_uuid),
                "type": "refresh",
                "token_version": configs.TOKEN_VERSION,
            },
            expires_in=configs.REFRESH_TOKEN_EXPIRES_IN,
            additional_claims=additional_claims,
            auth_config=configs,
        )

    @classmethod
    def decode_token(
        cls,
        token: str,
        verify_type: str | None = None,
        auth_config: AuthConfig | None = None,
    ) -> dict[str, Any]:
        """
        Decode and verify a JWT token with enhanced security checks.

        Args:
            token: JWT token to decode
            verify_type: Optional token type to verify
            auth_config: Optional auth configuration override

        Returns:
            dict: Decoded token payload

        Raises:
            TokenExpiredException: Token has expired
            InvalidTokenException: Token is invalid
        """
        import jwt
        from jwt.exceptions import (
            ExpiredSignatureError,
            InvalidAudienceError,
            InvalidIssuerError,
            InvalidSignatureError,
            InvalidTokenError,
        )

        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config
        required_claims = ["exp", "iat", "nbf", "aud", "iss", "sub", "type", "token_version"]
        if configs.ENABLE_JTI_CLAIM:
            required_claims.append("jti")

        try:
            payload = jwt.decode(
                token,
                configs.SECRET_KEY.get_secret_value(),
                algorithms=[configs.HASH_ALGORITHM],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "verify_aud": True,
                    "verify_iss": True,
                    "require": required_claims,
                },
                audience=configs.JWT_AUDIENCE,
                issuer=configs.JWT_ISSUER,
            )

            # Verify token type
            if verify_type and payload.get("type") != verify_type:
                raise InvalidTokenException(f"Invalid token type. Expected {verify_type}")

            # Verify token version
            if payload.get("token_version") != configs.TOKEN_VERSION:
                raise InvalidTokenException("Token version is outdated")

            return payload

        except ExpiredSignatureError as exception:
            raise TokenExpiredException("Token has expired") from exception
        except InvalidSignatureError as exception:
            raise InvalidTokenException("Token signature is invalid") from exception
        except InvalidAudienceError as exception:
            raise InvalidTokenException("Token has invalid audience") from exception
        except InvalidIssuerError as exception:
            raise InvalidTokenException("Token has invalid issuer") from exception
        except InvalidTokenError as exception:
            raise InvalidTokenException(f"Invalid token: {exception!s}") from exception

    @classmethod
    def verify_access_token(cls, token: str, auth_config: AuthConfig | None = None) -> dict[str, Any]:
        """Verify an access token."""
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config
        return cls.decode_token(token, verify_type="access", auth_config=configs)

    @classmethod
    def verify_refresh_token(cls, token: str, auth_config: AuthConfig | None = None) -> dict[str, Any]:
        """Verify a refresh token."""
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config
        return cls.decode_token(token, verify_type="refresh", auth_config=configs)

    @staticmethod
    def extract_user_uuid(payload: dict[str, Any]) -> UUID:
        """
        Extract user UUID from token payload.

        Args:
            payload: Decoded token payload

        Returns:
            UUID: User's UUID

        Raises:
            InvalidTokenException: If user identifier is invalid or missing
        """
        try:
            return UUID(payload["sub"])
        except (KeyError, ValueError) as exception:
            raise InvalidTokenException("Invalid or missing user identifier in token") from exception

    @classmethod
    def get_token_expiry(cls, token: str, auth_config: AuthConfig | None = None) -> int:
        """
        Get token expiry timestamp.

        Args:
            token: JWT token
            auth_config: Optional auth configuration override

        Returns:
            int: Token expiry timestamp in seconds

        Raises:
            InvalidTokenException: If token is invalid
        """
        payload = cls.decode_token(token, auth_config=auth_config)
        return int(payload["exp"])

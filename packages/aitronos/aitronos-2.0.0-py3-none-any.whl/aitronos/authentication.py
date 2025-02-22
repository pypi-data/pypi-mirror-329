"""
Authentication module for the Aitronos package.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional, Tuple

from aitronos.helper import perform_request, FreddyError, HTTPMethod, Config  # Updated to lowercase


class AuthenticationError(FreddyError):
    """Raised when authentication fails."""
    pass


@dataclass
class RefreshToken:
    """Data class for refresh token response."""
    token: str
    expiry: str


@dataclass
class LoginResponse:
    """Data class for login response."""
    token: str
    refresh_token: RefreshToken


class AuthenticationManager:
    """Handles authentication with the Aitronos API."""

    def __init__(self, base_url: str):
        """
        Initialize the authentication manager.

        Args:
            base_url (str): The base URL for the API.
        """
        self.base_url = base_url
        self.config = Config(base_url=base_url, backend_key="")  # Empty key for initial auth

    def validate_and_process_credentials(
        self,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Tuple[str, bool]:
        """
        Validate and process the provided credentials.

        Args:
            api_key (str, optional): API token for authentication.
            username (str, optional): Username for authentication.
            password (str, optional): Password for authentication.

        Returns:
            Tuple[str, bool]: A tuple containing the user token and a boolean indicating if it's a secret key.

        Raises:
            ValueError: If neither api_key nor both username and password are provided.
            AuthenticationError: If authentication fails or returns invalid response.
        """
        if api_key:
            # Check if it's a secret key (starts with 'sk')
            if api_key.startswith('sk'):
                return api_key, True
            return api_key, False
        elif username and password:
            return self._login_with_credentials(username, password), False
        else:
            raise ValueError(
                "You must provide either an API key or valid username and password."
            )

    def _login_with_credentials(self, username: str, password: str) -> str:
        """
        Authenticate with username and password.

        Args:
            username (str): Username for authentication.
            password (str): Password for authentication.

        Returns:
            str: The user token.

        Raises:
            AuthenticationError: If authentication fails or returns invalid response.
        """
        try:
            response = perform_request(
                method=HTTPMethod.POST,
                endpoint="/auth/login",
                config=self.config,
                body={
                    "emailOrUserName": username,
                    "password": password
                }
            )

            # Parse the response
            try:
                data = response.json()
                if not isinstance(data, dict):
                    raise AuthenticationError(AuthenticationError.Type.INVALID_RESPONSE, "Invalid response format")

                token = data.get("token")
                refresh_token = data.get("refreshToken", {})

                if not isinstance(token, str):
                    raise AuthenticationError(AuthenticationError.Type.INVALID_RESPONSE, "Invalid token format")

                if not isinstance(refresh_token, dict):
                    raise AuthenticationError(AuthenticationError.Type.INVALID_RESPONSE, "Invalid refresh token format")

                refresh_token_str = refresh_token.get("token")
                refresh_token_expiry = refresh_token.get("expiry")

                if not isinstance(refresh_token_str, str):
                    raise AuthenticationError(AuthenticationError.Type.INVALID_RESPONSE, "Invalid refresh token string format")

                if not isinstance(refresh_token_expiry, str):
                    raise AuthenticationError(AuthenticationError.Type.INVALID_RESPONSE, "Invalid refresh token expiry format")

                if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$', refresh_token_expiry):
                    raise AuthenticationError(AuthenticationError.Type.INVALID_RESPONSE, "Invalid refresh token expiry date format")

                return token

            except (json.JSONDecodeError, KeyError) as e:
                raise AuthenticationError(AuthenticationError.Type.INVALID_RESPONSE, f"Failed to parse authentication response: {str(e)}")

        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise e
            raise AuthenticationError(AuthenticationError.Type.INVALID_CREDENTIALS, str(e))

    def refresh_token(self, refresh_token: str) -> LoginResponse:
        """
        Refresh an expired token.

        Args:
            refresh_token (str): The refresh token to use.

        Returns:
            LoginResponse: The new token and refresh token.

        Raises:
            AuthenticationError: If token refresh fails or returns invalid response.
        """
        try:
            response = perform_request(
                method=HTTPMethod.POST,
                endpoint="/auth/refresh",
                config=self.config,
                body={"refresh_token": refresh_token}
            )

            try:
                data = response.json()
                if not isinstance(data, dict):
                    raise AuthenticationError("Invalid response format")

                token = data.get("token")
                refresh_token_data = data.get("refreshToken", {})

                if not isinstance(token, str):
                    raise AuthenticationError("Invalid token format")

                if not isinstance(refresh_token_data, dict):
                    raise AuthenticationError("Invalid refresh token format")

                refresh_token_str = refresh_token_data.get("token")
                refresh_token_expiry = refresh_token_data.get("expiry")

                if not isinstance(refresh_token_str, str):
                    raise AuthenticationError("Invalid refresh token string format")

                if not isinstance(refresh_token_expiry, str):
                    raise AuthenticationError("Invalid refresh token expiry format")

                if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$', refresh_token_expiry):
                    raise AuthenticationError("Invalid refresh token expiry date format")

                return LoginResponse(
                    token=token,
                    refresh_token=RefreshToken(
                        token=refresh_token_str,
                        expiry=refresh_token_expiry
                    )
                )

            except (json.JSONDecodeError, KeyError) as e:
                raise AuthenticationError(f"Failed to parse refresh token response: {str(e)}")

        except Exception as e:
            raise AuthenticationError(f"Token refresh failed: {str(e)}")

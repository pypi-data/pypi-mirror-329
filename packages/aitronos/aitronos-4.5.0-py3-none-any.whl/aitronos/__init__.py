"""
Aitronos Package

This package provides an API client for interacting with the Freddy Core API.
"""

from typing import Optional

from aitronos.helper import (
    Message,
    MessageRequestPayload,
    StreamEvent,
    is_valid_json,
    extract_json_strings,
    HTTPMethod,
    Config,
    FreddyError,
    perform_request,
)
from aitronos.StreamLine import StreamLine
from aitronos.authentication import (
    AuthenticationManager,
    LoginResponse,
    RefreshToken,
    AuthenticationError
)
from aitronos.assistant_messaging import AssistantMessaging
from aitronos.AppHive import (
    AppHiveError,
    Address,
    ProfileImage,
    UpdateUserProfileRequest
)

__version__ = "4.5.0"

# Expose CLI
from .cli import cli

__all__ = [
    # Main class
    "Aitronos",
    "Message",
    "MessageRequestPayload",
    "StreamEvent",
    
    # Authentication
    "LoginResponse",
    "RefreshToken",
    "AuthenticationError",
    
    # API Components
    "AssistantMessaging",
    "StreamLine",
    
    # Utility functions
    "is_valid_json",
    "extract_json_strings",
    
    # Types
    "HTTPMethod",
    "Config",
    "FreddyError",
    
    # AppHive
    "AppHiveError",
    "Address",
    "ProfileImage",
    "UpdateUserProfileRequest",
]


class Aitronos:
    """Main class for interacting with the Aitronos API."""

    BASE_URL = "https://freddy-api.aitronos.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize the Aitronos package.

        Args:
            api_key (str, optional): API token for authentication. This is the recommended authentication method.
                If the token starts with 'sk', it will be used as an API key in the header.
            username (str, optional): Username or email for authentication. Only use if you don't have an API key.
            password (str, optional): Password for authentication. Only use if you don't have an API key.

        Raises:
            ValueError: If neither api_key nor both username and password are provided.
            AuthenticationError: If authentication fails or returns invalid response.

        Note:
            It is recommended to use an API key for authentication instead of username/password.
            You can obtain an API key from your Aitronos dashboard.
        """
        if not api_key and not (username and password):
            raise ValueError("You must provide either an API key or valid username and password.")
        auth_manager = AuthenticationManager(base_url=self.BASE_URL)
        self._user_token, self._is_secret_key = auth_manager.validate_and_process_credentials(
            api_key=api_key,
            username=username,
            password=password
        )
        
        # Initialize API components
        self._assistant_messaging = None
        self._app_hive = None

    @property
    def assistant_messaging(self) -> AssistantMessaging:
        """
        Get an instance of the AssistantMessaging class, initialized with the API token.
        
        Returns:
            AssistantMessaging: The AssistantMessaging instance.
            
        Raises:
            ValueError: If user token is not available.
        """
        if not self._user_token:
            raise ValueError("User token is not available. Please authenticate first.")
            
        if self._assistant_messaging is None:
            self._assistant_messaging = AssistantMessaging(
                user_token=self._user_token,
                is_secret_key=self._is_secret_key
            )
            
        return self._assistant_messaging

    @property
    def AppHive(self):
        """
        Get an instance of the AppHive class, initialized with the API token.
        
        Returns:
            AppHive: The AppHive instance.
            
        Raises:
            ValueError: If user token is not available.
        """
        if not self._user_token:
            raise ValueError("User token is not available. Please authenticate first.")
            
        if self._app_hive is None:
            from aitronos.AppHive import AppHive
            self._app_hive = AppHive(
                user_token=self._user_token,
                is_secret_key=self._is_secret_key
            )
            
        return self._app_hive

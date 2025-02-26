"""
AppHive module for the Aitronos package.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class AppHiveError(Exception):
    """Base exception for AppHive errors."""
    class Type(Enum):
        HTTP_ERROR = "httpError"
        INVALID_CREDENTIALS = "invalidCredentials"
        INVALID_REQUEST = "invalidRequest"
        INVALID_RESPONSE = "invalidResponse"
        NETWORK_ERROR = "networkError"
        SERVER_ERROR = "serverError"
        UNKNOWN_ERROR = "unknownError"

    def __init__(self, error_type: Type, message: str):
        self.error_type = error_type
        super().__init__(f"{error_type.value}: {message}")


@dataclass
class Address:
    """Data class for address information."""
    street: str
    city: str
    state: str
    postal_code: str
    country: str


@dataclass
class ProfileImage:
    """Data class for profile image information."""
    url: str
    width: int
    height: int


@dataclass
class UpdateUserProfileRequest:
    """Data class for user profile update request."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Address] = None
    profile_image: Optional[ProfileImage] = None


class AppHive:
    """Main class for interacting with the AppHive API."""

    def __init__(self, user_token: str, is_secret_key: bool = False):
        """
        Initialize the AppHive class.

        Args:
            user_token (str): The authentication token for API requests.
            is_secret_key (bool): Whether the token is a secret key.
        """
        if not user_token:
            raise ValueError("User token cannot be empty")
        self._user_token = user_token
        self._is_secret_key = is_secret_key
        self._base_url = "https://freddy-api.aitronos.com"

    @property
    def user_management(self):
        """Get the user management component."""
        from .user_management import UserManagement
        return UserManagement(
            user_token=self._user_token,
            is_secret_key=self._is_secret_key
        ) 
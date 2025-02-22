"""
User management module for the AppHive API.
"""

from typing import Dict, Any, Optional
from aitronos.helper import perform_request, HTTPMethod, Config
from . import AppHiveError, Address, ProfileImage, UpdateUserProfileRequest


class UserManagement:
    """Class for managing user profiles and authentication."""

    def __init__(self, user_token: str, is_secret_key: bool = False):
        """
        Initialize the UserManagement class.

        Args:
            user_token (str): The authentication token for API requests.
            is_secret_key (bool): Whether the token is a secret key.
        """
        if not user_token:
            raise ValueError("User token cannot be empty")
        self._user_token = user_token
        self._is_secret_key = is_secret_key
        self._base_url = "https://freddy-api.aitronos.com"
        self._config = Config(base_url=self._base_url, backend_key=user_token)

    def check_username_duplication(self, user_id: str, username: str) -> bool:
        """
        Check if a username is already taken.

        Args:
            user_id (str): The user ID.
            username (str): The username to check.

        Returns:
            bool: True if the username is available, False if it's taken.

        Raises:
            AppHiveError: If the request fails.
        """
        try:
            response = perform_request(
                method=HTTPMethod.POST,
                endpoint="/api/users/check-username",
                config=self._config,
                body={
                    "userId": user_id,
                    "userName": username
                }
            )
            return response.json().get("available", False)
        except Exception as e:
            raise AppHiveError(AppHiveError.Type.HTTP_ERROR, str(e))

    def get_basic_user_profile(self) -> Dict[str, Any]:
        """
        Get the basic user profile.

        Returns:
            Dict[str, Any]: The basic user profile.

        Raises:
            AppHiveError: If the request fails.
        """
        try:
            response = perform_request(
                method=HTTPMethod.GET,
                endpoint="/v1/api/users/profile/basic",
                config=self._config
            )
            return response.json()
        except Exception as e:
            raise AppHiveError(AppHiveError.Type.HTTP_ERROR, str(e))

    def get_detailed_user_profile(self) -> Dict[str, Any]:
        """
        Get the detailed user profile.

        Returns:
            Dict[str, Any]: The detailed user profile.

        Raises:
            AppHiveError: If the request fails.
        """
        try:
            response = perform_request(
                method=HTTPMethod.GET,
                endpoint="/v1/api/users/profile/detailed",
                config=self._config
            )
            return response.json()
        except Exception as e:
            raise AppHiveError(AppHiveError.Type.HTTP_ERROR, str(e))

    def register_user(
        self,
        email: str,
        password: str,
        full_name: str,
        username: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new user.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            full_name (str): The user's full name.
            username (str, optional): The user's username.

        Returns:
            Dict[str, Any]: The registration response.

        Raises:
            AppHiveError: If the request fails.
        """
        try:
            data = {
                "email": email,
                "password": password,
                "fullName": full_name
            }
            if username:
                data["userName"] = username

            response = perform_request(
                method=HTTPMethod.POST,
                endpoint="/v1/api/users/register",
                config=self._config,
                body=data
            )
            return response.json()
        except Exception as e:
            raise AppHiveError(AppHiveError.Type.HTTP_ERROR, str(e))

    def update_username(self, user_id: str, user_name: str) -> bool:
        """
        Update a user's username.

        Args:
            user_id (str): The user ID.
            user_name (str): The new username.

        Returns:
            bool: True if the update was successful.

        Raises:
            AppHiveError: If the request fails.
        """
        try:
            response = perform_request(
                method=HTTPMethod.PUT,
                endpoint=f"/v1/api/users/{user_id}/username",
                config=self._config,
                body={"userName": user_name}
            )
            return response.status_code == 200
        except Exception as e:
            raise AppHiveError(AppHiveError.Type.HTTP_ERROR, str(e))

    def update_user_profile(self, profile: UpdateUserProfileRequest) -> None:
        """
        Update a user's profile.

        Args:
            profile (UpdateUserProfileRequest): The profile data to update.

        Raises:
            AppHiveError: If the request fails.
        """
        try:
            perform_request(
                method=HTTPMethod.PUT,
                endpoint="/v1/api/users/profile",
                config=self._config,
                body=profile.to_dict()
            )
        except Exception as e:
            raise AppHiveError(AppHiveError.Type.HTTP_ERROR, str(e)) 
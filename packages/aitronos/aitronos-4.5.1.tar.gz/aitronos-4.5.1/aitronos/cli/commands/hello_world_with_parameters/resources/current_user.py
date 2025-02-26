import json
from pathlib import Path
from typing import Optional
from .helpers import User


class CurrentUser:
    """
    A singleton-like class for managing the current user's data.
    Loads user data from a JSON file and provides access to the user's profile.
    """

    _instance = None
    _user_data: Optional[User] = None

    def __new__(cls):
        """
        Ensures only one instance of CurrentUser is created.
        """
        if cls._instance is None:
            cls._instance = super(CurrentUser, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Loads user data from a JSON file.
        """
        # Resolve the JSON file path relative to this file's location
        json_file = Path(__file__).parent / "user_data.json"

        if not json_file.exists():
            raise FileNotFoundError(f"JSON file not found at path: {json_file}")

        try:
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self._user_data = User.from_json(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading user data: {e}")

    @property
    def user(self) -> User:
        """
        Returns the current user's data.

        :return: An instance of the User class populated with data from the JSON file.
        """
        if self._user_data is None:
            raise RuntimeError("User data has not been initialized.")
        return self._user_data

    def reload(self):
        """
        Reloads the user data from the JSON file.
        """
        self._initialize()


# Example Usage
# if __name__ == "__main__":
#     try:
#         current_user = CurrentUser()  # Automatically loads user_data.json
#         user_data = current_user.user  # Access the User instance
#         print(user_data)
#     except Exception as e:
#         print(f"An error occurred: {e}")

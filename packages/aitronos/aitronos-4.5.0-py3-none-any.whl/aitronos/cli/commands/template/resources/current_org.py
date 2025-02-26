import json
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Address:
    """Organization address information."""
    street: str
    post_code: str
    city: str
    country: str
    phone_number: Optional[str] = None

    @staticmethod
    def from_json(data: dict) -> "Address":
        """Convert JSON data to Address instance."""
        return Address(
            street=data["street"],
            post_code=data["postCode"],
            city=data["city"],
            country=data["country"],
            phone_number=data.get("phoneNumber")
        )


@dataclass
class Organization:
    """Organization data structure."""
    id: str
    name: str
    logo: str
    address: Address
    members: List[str]
    created_at: datetime
    assistants: List[str]
    default_assistant: str

    @staticmethod
    def from_json(data: dict) -> "Organization":
        """Convert JSON data to Organization instance."""
        return Organization(
            id=data["id"],
            name=data["name"],
            logo=data["logo"],
            address=Address.from_json(data["address"]),
            members=data["members"],
            created_at=datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ"),
            assistants=data["assistants"],
            default_assistant=data["defaultAssistant"]
        )


class CurrentOrg:
    """
    A singleton-like class for managing the current organization's data.
    Loads organization data from a JSON file and provides access to the organization's profile.
    """

    _instance = None
    _org_data: Optional[Organization] = None

    def __new__(cls):
        """Ensures only one instance of CurrentOrg is created."""
        if cls._instance is None:
            cls._instance = super(CurrentOrg, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Loads organization data from a JSON file."""
        # Resolve the JSON file path relative to this file's location
        json_file = Path(__file__).parent / "org_data.json"

        if not json_file.exists():
            raise FileNotFoundError(f"JSON file not found at path: {json_file}")

        try:
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self._org_data = Organization.from_json(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading organization data: {e}")

    @property
    def org(self) -> Organization:
        """
        Returns the current organization's data.

        :return: An instance of the Organization class populated with data from the JSON file.
        :raises RuntimeError: If organization data has not been initialized.
        """
        if self._org_data is None:
            raise RuntimeError("Organization data has not been initialized.")
        return self._org_data

    def reload(self):
        """Reloads the organization data from the JSON file."""
        self._initialize()


# Example Usage
# if __name__ == "__main__":
#     try:
#         current_org = CurrentOrg()  # Automatically loads org_data.json
#         org_data = current_org.org  # Access the Organization instance
#         print(f"Organization: {org_data.name}")
#         print(f"Members: {len(org_data.members)}")
#         print(f"Assistants: {len(org_data.assistants)}")
#         print(f"Default Assistant: {org_data.default_assistant}")
#     except Exception as e:
#         print(f"An error occurred: {e}") 
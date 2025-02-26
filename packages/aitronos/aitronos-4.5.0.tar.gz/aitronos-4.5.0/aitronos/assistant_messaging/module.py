"""
AssistantMessaging module for interacting with the Aitronos Assistant API.
"""

import logging
import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Union, Callable
import requests
from aitronos.helper import Message, MessageRequestPayload, StreamEvent, is_valid_json

# Set up basic logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class AssistantMessaging:
    """Class for interacting with the Aitronos Assistant Messaging API."""

    def __init__(self, user_token: str, is_secret_key: bool = False):
        """
        Initialize the AssistantMessaging class.

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
    def base_url(self) -> str:
        """Get the base URL for API requests."""
        return self._base_url

    @property
    def user_token(self) -> str:
        """Get the user token."""
        return self._user_token

    def _get_auth_header(self) -> str:
        """Returns the appropriate authorization header based on token type."""
        if self._is_secret_key:
            return f"{self.user_token}"
        return f"Bearer {self.user_token}"

    def create_stream(self, payload: MessageRequestPayload, callback: Callable[[StreamEvent], None]) -> None:
        """
        Creates a streaming request to the run-stream endpoint.

        Args:
            payload: The message request payload.
            callback: Function to handle stream events.
        """
        url = f"{self.base_url}/messages/run-stream"
        headers = {
            "Authorization": self._get_auth_header(),
            "Content-Type": "application/json"
        }
        data = payload.to_dict()

        try:
            response = requests.post(url, json=data, headers=headers, stream=True)
            response.raise_for_status()

            buffer = ""
            for chunk in response.iter_content(decode_unicode=True):
                buffer += chunk.decode('utf-8')
                matches = list(re.finditer(self.JSON_PATTERN, buffer))

                for match in matches:
                    json_str = match.group()
                    try:
                        json_data = json.loads(json_str)
                        event = StreamEvent.from_json(json_data)
                        callback(event)
                    except json.JSONDecodeError as e:
                        log.error(f"Failed to decode JSON: {e}")

                buffer = buffer[matches[-1].end():] if matches else buffer

        except requests.RequestException as e:
            log.error(f"Request to {url} failed. Error details: {e}")
            raise Exception(f"Network or connection error while making request to {url}. Details: {e}")

    def execute_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
        """
        Executes a non-streaming run request.

        Args:
            payload: The message request payload.

        Returns:
            The API response as a dictionary, or None if the response is empty.
        """
        url = f"{self.base_url}/messages/run-stream"
        headers = {
            "Authorization": self._get_auth_header(),
            "Content-Type": "application/json"
        }
        data = payload.to_dict()
        data["stream"] = False

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            log.error(f"Error occurred while making request to {url}. Details: {e}")
            raise Exception(f"Network or connection error during API request. Details: {e}")

import re
import json
from enum import Enum
from typing import Optional, Any, Dict, List, Union, Callable
import logging
import requests

log = logging.getLogger(__name__)

__all__ = [
    "StreamEvent", "Message", "MessageRequestPayload", "is_valid_json", "extract_json_strings", "HTTPMethod", "Config",
    "FreddyError", "perform_request"
]


# MARK: - StreamEvent Class
class StreamEvent:
    class Event(Enum):
        THREAD_RUN_CREATED = "thread.run.created"
        THREAD_RUN_QUEUED = "thread.run.queued"
        THREAD_RUN_IN_PROGRESS = "thread.run.in_progress"
        THREAD_RUN_STEP_CREATED = "thread.run.step.created"
        THREAD_RUN_STEP_IN_PROGRESS = "thread.run.step.in_progress"
        THREAD_MESSAGE_CREATED = "thread.message.created"
        THREAD_MESSAGE_IN_PROGRESS = "thread.message.in_progress"
        THREAD_MESSAGE_DELTA = "thread.message.delta"
        THREAD_MESSAGE_COMPLETED = "thread.message.completed"
        THREAD_RUN_STEP_COMPLETED = "thread.run.step.completed"
        THREAD_RUN_COMPLETED = "thread.run.completed"
        OTHER = "other"

        @classmethod
        def from_raw(cls, raw_value: str):
            for event in cls:
                if event.value == raw_value:
                    return event
            return cls.OTHER

    class Status(Enum):
        QUEUED = "queued"
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"
        OTHER = "other"

        @classmethod
        def from_raw(cls, raw_value: str):
            for status in cls:
                if status.value == raw_value:
                    return status
            return cls.OTHER

    def __init__(self, event: Event, status: Optional[Status], is_response: bool, response: Optional[str],
                 thread_id: int):
        self.event = event
        self.status = status
        self.is_response = is_response
        self.response = response
        self.thread_id = thread_id

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> Optional['StreamEvent']:
        try:
            event = cls.Event.from_raw(json_data["event"])
            is_response = json_data["isResponse"]
            thread_id = json_data["threadId"]
            status = cls.Status.from_raw(json_data.get("status")) if "status" in json_data else None
            response = json_data.get("response")
            return cls(event, status, is_response, response, thread_id)
        except KeyError:
            log.error("Invalid JSON structure for StreamEvent.")
            return None


# MARK: - Message Class
class Message:
    def __init__(self, content: str, role: str, type: str = "text"):
        self.content = content
        self.role = role
        self.type = type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "role": self.role,
            "type": self.type
        }


# MARK: - MessageRequestPayload Class
class MessageRequestPayload:
    def __init__(self, organization_id: int, assistant_id: int, thread_id: Optional[int] = None,
                 model: str = "ftg-1.5", instructions: Optional[str] = None,
                 additional_instructions: Optional[str] = None, messages: List[Message] = [],
                 tool_choice: str = "auto"):
        self.organization_id = organization_id
        self.assistant_id = assistant_id
        self.thread_id = thread_id
        self.model = model
        self.instructions = instructions
        self.additional_instructions = additional_instructions
        self.messages = messages
        self.tool_choice = tool_choice

    def to_dict(self) -> Dict[str, Any]:
        # Create the dictionary and remove keys with `None` values
        payload = {
            "organization_id": self.organization_id,
            "assistant_id": self.assistant_id,
            "thread_id": self.thread_id,
            "model": self.model,
            "tool_choice": self.tool_choice,
            "instructions": self.instructions,
            "additional_instructions": self.additional_instructions,
            "messages": [message.to_dict() for message in self.messages]
        }
        # Filter out keys with None values
        return {key: value for key, value in payload.items() if value is not None}


# MARK: - Helper Functions

def is_valid_json(data: str) -> bool:
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False


def extract_json_strings(buffer: str, pattern: str = r'\{[^{}]*\}|\[[^\[\]]*\]') -> List[str]:
    return re.findall(pattern, buffer)


# MARK: - HTTPMethod Enum
class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


# MARK: - Config Class
class Config:
    def __init__(self, base_url: str, backend_key: str):
        self.base_url = base_url
        self.backend_key = backend_key


# MARK: - FreddyError Enum
class FreddyError(Exception):
    class Type(Enum):
        INVALID_URL = "invalidURL"
        INVALID_RESPONSE = "invalidResponse"
        HTTP_ERROR = "httpError"
        NO_DATA = "noData"
        DECODING_ERROR = "decodingError"
        NETWORK_ISSUE = "networkIssue"
        NO_USER_FOUND = "noUserFound"
        INCORRECT_PASSWORD = "incorrectPassword"
        INVALID_CREDENTIALS = "invalidCredentials"

    def __init__(self, error_type: Type, description: Optional[str] = None):
        self.error_type = error_type
        self.description = description or ""

    @classmethod
    def no_data(cls) -> "FreddyError":
        return cls(cls.Type.NO_DATA, "No data received from server")


# MARK: - perform_request Function
def perform_request(
    endpoint: str,
    method: HTTPMethod,
    config: Config,
    body: Optional[Dict[str, Any]] = None,
    empty_response: bool = False,
    callback: Callable[[Union[Any, FreddyError]], None] = None,
) -> requests.Response:
    """
    Performs an HTTP request and processes the response.

    :param endpoint: The API endpoint to call.
    :param method: HTTP method ("GET", "POST", etc.).
    :param config: Config object containing base_url and backend_key.
    :param body: Request body as a dictionary.
    :param empty_response: Whether the response is expected to be empty.
    :param callback: A function to handle the result.
    :return: The response object.
    """
    url = f"{config.base_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.backend_key}"
    }

    try:
        response = requests.request(
            method=method.value,
            url=url,
            headers=headers,
            json=body
        )

        if response.status_code < 200 or response.status_code > 299:
            try:
                error_details = response.json().get("error", "Unknown Error")
            except json.JSONDecodeError:
                error_details = response.text
            error = FreddyError(FreddyError.Type.HTTP_ERROR, f"{response.status_code}: {error_details}")
            if callback:
                callback(error)
            raise error

        if empty_response:
            if callback:
                callback(None)
            return response

        try:
            data = response.json()
            if callback:
                callback(data)
            return response
        except json.JSONDecodeError as e:
            error = FreddyError(FreddyError.Type.DECODING_ERROR, str(e))
            if callback:
                callback(error)
            raise error

    except requests.exceptions.RequestException as e:
        error = FreddyError(FreddyError.Type.NETWORK_ISSUE, str(e))
        if callback:
            callback(error)
        raise error
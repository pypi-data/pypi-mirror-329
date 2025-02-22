"""
Tests for the AssistantMessaging module using real API requests.
"""

import unittest
from config import Config
from typing import List
from aitronos import (
    AssistantMessaging,
    Message,
    MessageRequestPayload,
    StreamEvent,
    AppHiveError,
    AssistantMessagingError
)


class TestAssistantMessaging(unittest.TestCase):
    """Test cases for the AssistantMessaging class using real API calls."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are shared across all tests."""
        try:
            cls.test_api_key = Config.test_key()
            cls.test_org_id = Config.test_org_id()
            cls.test_assistant_id = Config.test_assistant_id()
        except (FileNotFoundError, KeyError) as e:
            raise unittest.SkipTest(
                f"Skipping AssistantMessaging tests: {str(e)}"
            )

    def setUp(self):
        """Set up test fixtures."""
        self.client = AssistantMessaging(
            user_token=self.test_api_key,
            is_secret_key=self.test_api_key.startswith("sk")
        )
        self.base_payload = MessageRequestPayload(
            organization_id=self.test_org_id,
            assistant_id=self.test_assistant_id,
            messages=[
                Message(content="Hello, how are you?", role="user")
            ]
        )

    def test_initialization(self):
        """Test initialization of AssistantMessaging."""
        self.assertEqual(self.client.user_token, self.test_api_key)
        self.assertEqual(self.client.base_url, "https://freddy-api.aitronos.com")

    def test_execute_run(self):
        """Test non-streaming message execution."""
        response = self.client.execute_run(self.base_payload)
        
        # Verify response structure
        self.assertIsInstance(response, dict)
        self.assertIn("response", response)
        self.assertIsInstance(response["response"], str)
        self.assertGreater(len(response["response"]), 0)

    def test_create_stream(self):
        """Test streaming message execution."""
        events: List[StreamEvent] = []

        def callback(event: StreamEvent):
            events.append(event)

        self.client.create_stream(self.base_payload, callback)

        # Verify we received events
        self.assertGreater(len(events), 0)
        
        # Verify event structure
        for event in events:
            self.assertIsInstance(event, StreamEvent)
            self.assertIsInstance(event.event, StreamEvent.Event)
            if event.status:
                self.assertIsInstance(event.status, StreamEvent.Status)
            if event.response:
                self.assertIsInstance(event.response, str)

        # Verify we got a completion
        completion_events = [e for e in events if e.event == StreamEvent.Event.THREAD_MESSAGE_COMPLETED]
        self.assertGreater(len(completion_events), 0)

    def test_complex_conversation(self):
        """Test a more complex conversation with multiple messages."""
        messages = [
            Message(content="What is machine learning?", role="user"),
            Message(content="Can you explain it in simpler terms?", role="user")
        ]
        
        payload = MessageRequestPayload(
            organization_id=self.test_org_id,
            assistant_id=self.test_assistant_id,
            messages=messages
        )
        
        response = self.client.execute_run(payload)
        self.assertIsInstance(response, dict)
        self.assertIn("response", response)
        self.assertIsInstance(response["response"], str)
        self.assertGreater(len(response["response"]), 0)

    def test_invalid_request(self):
        """Test handling of invalid requests."""
        # Test with invalid organization ID
        invalid_payload = MessageRequestPayload(
            organization_id=-1,  # Invalid org ID
            assistant_id=self.test_assistant_id,
            messages=[Message(content="Test", role="user")]
        )
        
        with self.assertRaises(Exception) as context:
            self.client.execute_run(invalid_payload)
        self.assertIn("error", str(context.exception).lower())

    def test_empty_message(self):
        """Test handling of empty messages."""
        empty_payload = MessageRequestPayload(
            organization_id=self.test_org_id,
            assistant_id=self.test_assistant_id,
            messages=[Message(content="", role="user")]
        )
        
        with self.assertRaises(Exception) as context:
            self.client.execute_run(empty_payload)
        self.assertIn("error", str(context.exception).lower())

    def test_streaming_interruption(self):
        """Test handling of streaming interruption."""
        events: List[StreamEvent] = []
        interrupted = False

        def callback(event: StreamEvent):
            nonlocal interrupted
            events.append(event)
            if len(events) > 2 and not interrupted:
                interrupted = True
                raise KeyboardInterrupt()

        try:
            self.client.create_stream(self.base_payload, callback)
        except KeyboardInterrupt:
            pass

        # Verify we received some events before interruption
        self.assertGreater(len(events), 0)
        self.assertTrue(interrupted)


if __name__ == '__main__':
    unittest.main() 
"""
Tests for the Aitronos package initialization.
"""

import unittest
from unittest.mock import patch, MagicMock
from config import Config

from aitronos import (
    Aitronos,
    AssistantMessaging,
    AuthenticationError,
    Message,
    MessageRequestPayload,
    AppHiveError
)


class TestAitronosPackage(unittest.TestCase):
    """Test cases for the Aitronos package initialization."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are shared across all tests."""
        try:
            cls.test_api_key = Config.test_key()
            cls.test_username = Config.test_username()
            cls.test_password = Config.test_password()
        except (FileNotFoundError, KeyError) as e:
            raise unittest.SkipTest(
                f"Skipping package init tests: {str(e)}"
            )

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = Aitronos(api_key=self.test_api_key)
        self.assertIsNotNone(client._user_token)
        self.assertEqual(client._user_token, self.test_api_key)
        self.assertEqual(client._is_secret_key, self.test_api_key.startswith("sk"))

    def test_init_with_credentials(self):
        """Test initialization with username and password."""
        client = Aitronos(
            username=self.test_username,
            password=self.test_password
        )
        self.assertIsNotNone(client._user_token)
        self.assertFalse(client._is_secret_key)

    def test_init_without_credentials(self):
        """Test initialization without any credentials."""
        with self.assertRaises(ValueError) as context:
            Aitronos()
        self.assertIn("You must provide either an API key or valid username and password", str(context.exception))

    def test_init_with_invalid_credentials(self):
        """Test initialization with invalid credentials."""
        with self.assertRaises(AuthenticationError) as context:
            Aitronos(username=self.test_username, password="wrong_password")
        self.assertEqual(context.exception.error_type, AuthenticationError.Type.INVALID_CREDENTIALS)

    def test_assistant_messaging_property(self):
        """Test the assistant_messaging property."""
        client = Aitronos(api_key=self.test_api_key)
        
        # First access should create new instance
        messaging = client.assistant_messaging
        self.assertIsInstance(messaging, AssistantMessaging)
        self.assertEqual(messaging.user_token, self.test_api_key)
        
        # Second access should return cached instance
        messaging2 = client.assistant_messaging
        self.assertIs(messaging, messaging2)  # Should be the exact same instance

    def test_base_url_constant(self):
        """Test the BASE_URL class constant."""
        self.assertEqual(
            Aitronos.BASE_URL,
            "https://freddy-api.aitronos.com"
        )

    def test_version_attribute(self):
        """Test the package version attribute."""
        from aitronos import __version__
        self.assertIsInstance(__version__, str)
        self.assertRegex(__version__, r'^\d+\.\d+\.\d+$')

    def test_property_access_without_token(self):
        """Test accessing properties when token is not available."""
        client = Aitronos(api_key=self.test_api_key)
        client._user_token = None  # Simulate missing token
        
        with self.assertRaises(ValueError) as context:
            _ = client.assistant_messaging
        self.assertIn("User token is not available", str(context.exception))


if __name__ == '__main__':
    unittest.main()

# Different ways to run these tests:

# 1. Run all tests in this file:
# python -m pytest tests/test_package_init.py
# pytest tests/test_package_init.py

# 2. Run a specific test class:
# python -m pytest tests/test_package_init.py::TestAitronosPackage
# pytest tests/test_package_init.py::TestAitronosPackage

# 3. Run a specific test method:
# python -m pytest tests/test_package_init.py::TestAitronosPackage::test_init_with_api_key
# pytest tests/test_package_init.py::TestAitronosPackage::test_init_with_api_key

# 4. Run with unittest directly:
# python -m unittest tests/test_package_init.py
# python tests/test_package_init.py

# 5. Run with verbose output:
# pytest -v tests/test_package_init.py
# python -m pytest -v tests/test_package_init.py

# 6. Run and stop on first failure:
# pytest -x tests/test_package_init.py

# 7. Run with print output:
# pytest -s tests/test_package_init.py

# 8. Run and show local variables on failure:
# pytest -l tests/test_package_init.py

# 9. Run with test coverage:
# pytest --cov=aitronos tests/test_package_init.py

# 10. Run tests matching a pattern:
# pytest -k "api" tests/test_package_init.py  # runs tests with "api" in the name

# 11. Run tests and create HTML report:
# pytest --html=report.html tests/test_package_init.py

# 12. Using update_version.py script:
# python update_version.py patch  # Runs all tests before version bump
# python update_version.py patch --skip-tests  # Skips tests

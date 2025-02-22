"""
Tests for the authentication module.

These tests use real API calls with credentials from config.json.
"""

import unittest
from config import Config
from aitronos.authentication import (
    AuthenticationManager,
    LoginResponse,
    RefreshToken,
    AuthenticationError
)


class TestAuthenticationManager(unittest.TestCase):
    """Test cases for the AuthenticationManager class."""

    BASE_URL = "https://freddy-api.aitronos.com"

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are shared across all tests."""
        try:
            cls.test_username = Config.test_username()
            cls.test_password = Config.test_password()
            cls.test_api_key = Config.test_key()
        except (FileNotFoundError, KeyError) as e:
            raise unittest.SkipTest(
                f"Skipping live authentication tests: {str(e)}"
            )

    def setUp(self):
        """Set up test fixtures."""
        self.auth = AuthenticationManager(base_url=self.BASE_URL)

    def test_successful_login(self):
        """Test successful login with valid credentials."""
        token, is_secret = self.auth.validate_and_process_credentials(
            username=self.test_username,
            password=self.test_password
        )

        # Verify response structure
        self.assertIsInstance(token, str)
        self.assertFalse(is_secret)
        self.assertTrue(token)  # Token should not be empty

    def test_failed_login(self):
        """Test login with invalid credentials."""
        with self.assertRaises(AuthenticationError):
            self.auth.validate_and_process_credentials(
                username=self.test_username,
                password="wrong_password"
            )

    def test_api_key_authentication(self):
        """Test authentication with API key."""
        token, is_secret = self.auth.validate_and_process_credentials(
            api_key=self.test_api_key
        )
        
        self.assertEqual(token, self.test_api_key)
        self.assertEqual(is_secret, self.test_api_key.startswith("sk"))

    def test_invalid_api_key(self):
        """Test authentication with invalid API key."""
        with self.assertRaises(ValueError):
            self.auth.validate_and_process_credentials(api_key="  ")

    def test_refresh_token(self):
        """Test refreshing a token."""
        # First get a valid token and refresh token
        token, _ = self.auth.validate_and_process_credentials(
            username=self.test_username,
            password=self.test_password
        )
        
        # Now try to refresh it
        response = self.auth.refresh_token(token)
        
        # Verify response structure
        self.assertIsInstance(response, LoginResponse)
        self.assertIsInstance(response.token, str)
        self.assertIsInstance(response.refresh_token, RefreshToken)
        self.assertIsInstance(response.refresh_token.token, str)
        self.assertIsInstance(response.refresh_token.expiry, str)

        # Verify non-empty values
        self.assertTrue(response.token)
        self.assertTrue(response.refresh_token.token)
        self.assertTrue(response.refresh_token.expiry)


if __name__ == '__main__':
    unittest.main()

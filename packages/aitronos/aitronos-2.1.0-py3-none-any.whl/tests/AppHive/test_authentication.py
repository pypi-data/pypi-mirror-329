import unittest
from unittest.mock import patch
from aitronos import Aitronos, LoginResponse, AppHiveError
from config import Config


class TestAuthentication(unittest.TestCase):
    """Test suite for the Authentication and Aitronos integration."""

    def setUp(self):
        """Set up test data and environment."""
        self.base_url = "https://freddy-api.aitronos.com"
        self.valid_email = Config.test_email()
        self.valid_password = Config.test_password()
        self.invalid_email = "wrong@example.com"
        self.invalid_password = "wrongpass"

    @patch("aitronos.helper.perform_request")
    def test_login_success_with_aitronos(self, mock_perform_request):
        """Test a successful login through Aitronos with credentials."""
        mock_perform_request.return_value = {
            "token": "mocked_token",
            "refreshToken": {"token": "mocked_refresh_token", "expiry": "2024-12-31T23:59:59Z"},
            "deviceId": "mocked_device_id",
        }

        # Simulate passing an API key directly
        aitronos = Aitronos(api_key="mocked_token")

        # Verify the token was stored correctly
        self.assertEqual(aitronos._user_token, "mocked_token")
        print("Mocked Login Successful! Retrieved Token:", aitronos._user_token)

    # @patch("Aitronos.helper.perform_request")
    # def test_login_invalid_credentials_with_aitronos(self, mock_perform_request):
    #     """Test login through Aitronos with invalid credentials."""
    #     # Mock perform_request to simulate an HTTP 401 error for invalid credentials
    #     mock_perform_request.side_effect = AppHiveError(
    #         AppHiveError.Type.HTTP_ERROR, "HTTP 404: {\"message\":\"User name not found\"}"
    #     )
    #
    #     with self.assertRaises(AppHiveError) as context:
    #         # Initialize Aitronos with invalid credentials
    #         Aitronos(username=self.invalid_email, password=self.invalid_password)
    #
    #     # Verify the type and message of the raised exception
    #     self.assertEqual(context.exception.error_type, AppHiveError.Type.HTTP_ERROR)
    #     self.assertEqual(str(context.exception), "httpError: HTTP 404: {\"message\":\"User name not found\"}")
    #     print("Test Passed: Invalid credentials raise the correct error.")

    def test_login_invalid_response_with_aitronos(self):
        """Test login through Aitronos with invalid inputs."""

        # Case 1: API key is empty
        with self.assertRaises(ValueError) as context:
            Aitronos(api_key="")
        self.assertEqual(context.exception.args[0],
                         "You must provide either an API key or valid username and password.")

        # Case 2: Username is empty
        with self.assertRaises(ValueError) as context:
            Aitronos(username="", password=self.valid_password)
        self.assertEqual(context.exception.args[0],
                         "You must provide either an API key or valid username and password.")

        # Case 3: Password is empty
        with self.assertRaises(ValueError) as context:
            Aitronos(username=self.valid_email, password="")
        self.assertEqual(context.exception.args[0],
                         "You must provide either an API key or valid username and password.")

        print("Test Passed: Invalid inputs raise ValueError as expected.")

    def test_login_success_real_request(self):
        """Test a successful login with real credentials through Aitronos."""
        try:
            aitronos = Aitronos(username=self.valid_email, password=self.valid_password)
            self.assertIsNotNone(aitronos._user_token, "Token should not be None")
            print("Real Login Successful!")
            print("Token:", aitronos._user_token)
        except AppHiveError as e:
            self.fail(f"Real login failed: {e}")


if __name__ == "__main__":
    unittest.main()
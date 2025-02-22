import unittest
from config import Config
from aitronos.AppHive import Address, ProfileImage, UpdateUserProfileRequest
from aitronos.AppHive import AppHiveError
from aitronos import Aitronos

class UserManagementTests(unittest.TestCase):
    """Test suite for the UserManagement class with real API calls."""

    def setUp(self):
        """Set up the test environment."""
        # Load credentials from the config file
        self.user_token = Config.user_token()
        self.user_management = Aitronos(api_key=self.user_token).AppHive.user_management

        # Set up test data
        self.test_user_id = Config.test_user_id()
        self.test_username = Config.test_username()
        self.test_email = Config.test_email()
        self.test_password = Config.test_password()
        self.test_full_name = Config.test_full_name()
        self.test_new_username = Config.test_username()

    def test_check_username_duplication(self):
        """Test checking if a username is already taken."""
        try:
            result = self.user_management.check_username_duplication(
                user_id=self.test_user_id, username=self.test_username
            )
            self.assertIsInstance(result, bool, "Result should be a boolean.")
            print(f"Check Username Duplication: {result}")
        except AppHiveError as e:
            self.fail(f"API call failed: {e}")

    def test_get_basic_user_profile(self):
        """Test fetching the basic user profile."""
        try:
            profile = self.user_management.get_basic_user_profile()
            self.assertIn("userName", profile, "Basic profile should contain 'userName'.")
            print(f"Basic User Profile: {profile}")
        except AppHiveError as e:
            self.fail(f"API call failed: {e}")

    def test_get_detailed_user_profile(self):
        """Test fetching the detailed user profile."""
        try:
            profile = self.user_management.get_detailed_user_profile()
            self.assertIn("userId", profile, "Detailed profile should contain 'userId'.")
            print(f"Detailed User Profile: {profile}")
        except AppHiveError as e:
            self.fail(f"API call failed: {e}")

    def test_register_user(self):
        """Test registering a new user."""
        try:
            response = self.user_management.register_user(
                email="test_register@example.com",
                password="SecurePassword123!",
                full_name="Test User",
            )
            self.assertIn("userId", response, "Response should contain 'userId'.")
            print(f"Register User Response: {response}")
        except AppHiveError as e:
            self.fail(f"API call failed: {e}")

    def test_update_username(self):
        """Test updating a user's username."""
        try:
            result = self.user_management.update_username(
                user_id=self.test_user_id, user_name=self.test_new_username
            )
            self.assertTrue(result, "Updating the username should return True.")
            print(f"Update Username Result: {result}")
        except AppHiveError as e:
            self.fail(f"API call failed: {e}")

    # def test_update_user_profile(self):
    #     """Test updating a user's profile."""
    #     profile_data = UpdateUserProfileRequest(
    #         full_name="Test User",
    #         last_name="LastName",
    #         user_name="testuser_updated",
    #         email="test_updated@example.com",
    #         address=Address(
    #             full_name="Test User",
    #             street="123 Test Street",
    #             post_code="12345",
    #             city="Test City",
    #             country=1,
    #             phone_number="1234567890"
    #         ),
    #         profile_image=ProfileImage(
    #             background="#FFFFFF",
    #             image="base64EncodedImageString"
    #         ),
    #         birthday="1990-01-01",
    #         gender=1,
    #         country=1,
    #         password="SecurePassword123!",
    #     )
    #
    #     try:
    #         self.user_management.update_user_profile(profile_data)
    #         print("Update User Profile: Success")
    #     except AppHiveError as e:
    #         self.fail(f"API call failed: {e}")


if __name__ == "__main__":
    unittest.main()
import unittest
from aitronos import MessageRequestPayload, Message, Aitronos, AppHiveError
from config import Config


class AuthenticationTests(unittest.TestCase):
    def test_authentication_with_valid_username_and_password(self):
        print("test_authentication_with_valid_username_and_password")
        user_name = Config.test_username()
        password = Config.test_password()
        try:
            print("username: ", user_name, "password: ", password)
            aitronos = Aitronos(username=user_name, password=password)
            print(aitronos)
        except Exception as e:
            print(e)
            self.fail(f"Authentication failed: {e}")
    
    def test_authentication_with_invalid_username(self):
        print("test_authentication_with_invalid_username_and_password")
        user_name = "InvalidUsername"
        password = Config.test_password()
        try:
            aitronos = Aitronos(username=user_name, password=password)
            self.fail("Authentication should have failed")
        except AppHiveError as e:
            self.assertIn("Authentication failed", str(e))
            
    def test_authentication_with_invalid_password(self):
        print("test_authentication_with_invalid_password")
        user_name = Config.test_username()
        password = "InvalidPassword"
        try:
            aitronos = Aitronos(username=user_name, password=password)
            self.fail("Authentication should have failed")
            # Start of Selection
        except AppHiveError as e:
            print(e)
            self.assertIn(
                "httpError: Authentication failed: httpError: HTTP 401: Unknown Error\n"
                "Please verify your credentials or use an API key instead.",
                str(e)
            )
            
    def test_authentication_with_api_key(self):
        print("test_authentication_with_api_key")
        api_key = Config.test_key()
        try:
            aitronos = Aitronos(api_key=api_key)
            print(aitronos)
        except Exception as e:
            print(e)
            self.fail(f"Authentication failed: {e}")
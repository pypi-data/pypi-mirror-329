class StreamLine:
    """
    A Python translation of the AppHive class.
    """

    def __init__(self, user_token: str):
        """
        Initialize the AppHive class with a user token.
        """
        if not user_token:
            raise ValueError("AppHive API Key cannot be empty")
        self._user_token = user_token

    @property
    def base_url(self) -> str:
        """
        A property that returns the base URL.
        """
        return "https://freddy-api.aitronos.com"

    @property
    def user_token(self) -> str:
        """
        A getter for the user token.
        """
        return self._user_token

    @user_token.setter
    def user_token(self, value: str):
        """
        A setter for the user token that ensures the token is not empty.
        """
        if not value:
            raise ValueError("AppHive API Key cannot be empty")
        self._user_token = value
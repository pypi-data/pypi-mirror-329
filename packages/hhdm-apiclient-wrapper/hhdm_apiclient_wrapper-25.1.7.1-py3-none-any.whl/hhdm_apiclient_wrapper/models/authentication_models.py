import datetime
from enum import Enum

class AuthenticationMode(Enum):
    OAUTH = 0
    API_KEY = 1

class AuthenticationSettings:
    def __init__(
            self,
            access_token: str = None,
            refresh_token: str = None,
            identity_token: str = None,
            access_token_expiry: datetime = None,
            authentication_mode: AuthenticationMode = None,
            api_key: str = None) -> None:
        self.access_token: str = access_token
        self.refresh_token: str = refresh_token
        self.identity_token: str = identity_token
        self.access_token_expiry: datetime = access_token_expiry
        self.authentication_mode: AuthenticationMode = authentication_mode
        self.api_key: str = api_key



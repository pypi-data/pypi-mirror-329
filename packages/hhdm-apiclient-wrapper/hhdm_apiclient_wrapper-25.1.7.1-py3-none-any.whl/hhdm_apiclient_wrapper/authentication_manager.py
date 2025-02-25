from asyncio import Future
from typing import Dict
from uuid import UUID

from hhdm_apiclient_wrapper.models.authentication_models import *
# import oauth_authentication_manager

class AuthenticationManager:
    def __init__(self, authentication_settings: AuthenticationSettings) -> None:
        self.authentication_settings = authentication_settings or AuthenticationSettings()

    async def get_http_request_auth(self) -> Future[Dict]:
        if not await self.check_api_authentication():
            return None
        
        match self.authentication_settings.authentication_mode:
            case AuthenticationMode.OAUTH:
                return {'Authorization': f'Bearer {self.authentication_settings.access_token}'}
            case AuthenticationMode.API_KEY:
                return {'ApiKey': self.authentication_settings.api_key}

        return None

    async def check_api_authentication(self) -> Future[bool]:
        if self.authentication_settings.authentication_mode == AuthenticationMode.API_KEY:
            return self.check_api_key(self.authentication_settings.api_key) 
        # TODO: Implement OAUTH Authentication
        return False
        # return await oauth_authentication_manager.check_authentication()
    
    def check_api_key(self, api_key: str) -> bool:
        try:
            uuid_obj = UUID(api_key)
        except ValueError:
            return False
        
        return str(uuid_obj) == api_key

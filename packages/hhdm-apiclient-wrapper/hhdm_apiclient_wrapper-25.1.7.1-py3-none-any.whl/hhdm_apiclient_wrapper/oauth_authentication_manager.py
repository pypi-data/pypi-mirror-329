from asyncio import Future
from datetime import datetime, timedelta

from hhdm_apiclient_wrapper.authentication_models import *

auth_host = 'https://auth.hh-dev.com/'
logout_url = 'https://hh-dev.com/signout-callback-oidc'
client_secret = '79c0e29e-978d-496e-95a8-4f9a1e111731'

authentication_settings = AuthenticationSettings()

def has_access_token_expired():
    return (datetime.now() + timedelta(minutes=5)) > authentication_settings.access_token_expiry

async def check_authentication() -> Future[bool]:
    if authentication_settings.access_token is None or len(authentication_settings.access_token) == 0:
        return await login_with_oauth()

    if has_access_token_expired():
        refresh_result = await refresh_access_token()
        if not refresh_result:
            return await login_with_oauth()
        
        return True
    
    return True

async def login_with_oauth() -> Future[bool]:
    port = 0

async def refresh_access_token() -> Future:
    pass


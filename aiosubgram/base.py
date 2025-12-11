import aiohttp
import asyncio
from typing import Optional, Dict, Type, TypeVar
from enum import Enum
from .exceptions import APIError, NetworkError, SubgramError, AuthError
from .types.base import SubgramObject

T = TypeVar("T", bound=SubgramObject)

class KeyType(Enum):
    SECRET = "secret"
    TOKEN = "token"
    BOT = "bot"

class BaseClient:
    API_URL = "https://api.subgram.org"

    def __init__(self, secret_key: Optional[str] = None, api_token: Optional[str] = None, api_key: Optional[str] = None,
                 timeout: Optional[float] = 15.0):
        self.secret_key = secret_key
        self.api_token = api_token
        self.api_key = api_key
        self.timeout = timeout
        if not any([secret_key, api_token, api_key]):
            raise AuthError()
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session
    
    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    def _get_auth_header(self, key_type: KeyType) -> Dict[str, str]:
        key = None
        
        if key_type == KeyType.SECRET:
            key = self.secret_key
        elif key_type == KeyType.TOKEN:
            key = self.api_token
        elif key_type == KeyType.BOT:
            key = self.api_key
            
        if not key:
            raise SubgramError(f"API Key of type '{key_type.value}' is not provided but required for this request.")

        return {"Auth": key}

    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        response_model: Type[T],
        key_type: KeyType = KeyType.SECRET,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> T:
        session = await self.get_session()
        url = f"{self.API_URL}/{endpoint}"
        
        headers = self._get_auth_header(key_type)

        try:
            async with session.request(method, url, params=params, json=json, headers=headers) as response:
                data = await response.json()
                
                if response.status >= 400 and data["status"] == "error":
                    raise APIError(response.status, f"API Subgram Error: {data}")
                
                return response_model.model_validate(data)
                
        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error occurred: {e}")
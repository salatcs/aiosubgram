from typing import Optional
import asyncio
from .base import BaseClient
from .methods import APIMethods

class SubgramClient(BaseClient, APIMethods):
    """
    Основной класс для взаимодействия с API.
    Наследуется от BaseClient для доступа к _make_request.
    """

    def __init__(self, secret_key: Optional[str] = None, api_token: Optional[str] = None, api_key: Optional[str] = None):
        """
        Экземпляр клиента Subgram.

        Args:
            secret_key: Secret Key (для управления заказами/ботами).
            api_token: API Token (для статистики/баланса).
            api_key: API Key бота (для работы с подписками/спонсорами).
        """
        super().__init__(secret_key, api_token, api_key)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()
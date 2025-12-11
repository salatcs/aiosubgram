from typing import Optional, Literal, Union
from datetime import date
from .base import MethodMixin
from ..base import KeyType
from ..types.general import (
    GetBalance,
    GetFilters,
    GetStatistic,
    ToggleExclusion
)

class GeneralMethods(MethodMixin):
    async def get_balance(self) -> GetBalance:
        """
        Возвращает текущий баланс аккаунта и краткую сводку по ботам.
        Требует `api_token`.

        Returns:
            GetBalance: Баланс и список ботов с их доходом.
        """
        return await self._make_request(
        method="POST",
        endpoint="get-balance",
        response_model=GetBalance,
        key_type=KeyType.TOKEN
        )
    
    async def get_filters(self) -> GetFilters:
        """
        Возвращает список всех доступных значений для таргетинга (страны, языки, тематики).
        Не требует авторизации (но метод использует токен, если он есть в клиенте).

        Returns:
            GetFilters: Списки фильтров для рекламодателей и владельцев ботов.
        """
        return await self._make_request(
            method="GET",
            endpoint="filters",
            response_model=GetFilters,
            key_type=KeyType.TOKEN
        )

    async def get_statistic(
        self,
        action: Literal["allads", "ads", "source", "allbots", "bots", "sponsor"],
        ads_id: Optional[int] = None,
        bot_id: Optional[int] = None,
        start_date: Optional[Union[date, str]] = None,
        end_date: Optional[Union[date, str]] = None
    ) -> GetStatistic:
        """
        Универсальный метод получения статистики доходов и расходов.
        Требует `api_token`.

        Args:
            action: Тип статистики (allads/ads/source для рекламодателей, allbots/bots/sponsor для владельцев).
            ads_id: ID заказа (обязательно для actions: ads, source).
            bot_id: ID бота (обязательно для actions: bots, sponsor).
            start_date: Начальная дата (по умолч. 9 дней назад).
            end_date: Конечная дата (по умолч. сегодня).

        Returns:
            GetStatistic: Объект со статистическими данными (графики, таблицы).
        """
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")

        params = {
            "api_token": self.api_token,
            "action": action,
            "ads_id": ads_id,
            "bot_id": bot_id,
            "start_date": start_date,
            "end_date": end_date,
            "output_format": "json"
        }
        
        request_params = {k: v for k, v in params.items() if v is not None}

        return await self._make_request(
            method="GET",
            endpoint="statistic",
            response_model=GetStatistic,
            params=request_params,
            key_type=KeyType.TOKEN
        )

    async def toggle_exclusion(
        self,
        action: Literal["exclude", "activate"],
        context: Literal["advertiser", "publisher"],
        ads_id: int,
        bot_id: Optional[int] = None
    ) -> ToggleExclusion:
        """
        Управление черными списками (исключение ботов или спонсоров).
        Требует `api_token`.

        Args:
            action: 'exclude' (добавить в ЧС) или 'activate' (убрать из ЧС).
            context: 'advertiser' (рекламодатель блочит бота) или 'publisher' (владелец бота блочит спонсора).
            ads_id: ID заказа (или ID спонсора в контексте publisher).
            bot_id: ID бота (обязателен для advertiser, опционален для publisher).

        Returns:
            ToggleExclusion: Статус операции.
        """
        params = {
            "api_token": self.api_token
        }
        
        payload = {
            "action": action,
            "context": context,
            "ads_id": ads_id,
            "bot_id": bot_id
        }
        
        json_data = {k: v for k, v in payload.items() if v is not None}

        return await self._make_request(
            method="POST",
            endpoint="toggle-exclusion",
            response_model=ToggleExclusion,
            params=params,
            json=json_data,
            key_type=KeyType.TOKEN
        )
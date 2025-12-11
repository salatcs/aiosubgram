from typing import List, Optional, Literal, Dict, Union
from .base import MethodMixin
from ..base import KeyType
from ..types.advertiser import (
    CreateOrder,
    OrderInfo,
    UserParameters,
    OrderSchedule
)
class AdvertiserMethods(MethodMixin):
    async def create_order(
        self,
        link: str,
        ads_type: Literal["channel", "bot", "resource"],
        quantity_all: int,
        name: Optional[str] = None,
        is_on: Optional[int] = 1,
        quantity_day: Optional[int] = None,
        price: Optional[float] = None,
        price_premium: Optional[float] = None,
        bot_token: Optional[str] = None,
        to_bot_member: Optional[int] = 0,
        track_unsubscriptions: Optional[bool] = True,
        is_lite: Optional[int] = 0,
        sub_speed: Optional[int] = None,
        user_parameters: Optional[Union[UserParameters, Dict]] = None,
        forbidden_themes: Optional[List[str]] = None,
        order_schedule: Optional[Union[OrderSchedule, Dict]] = None
    ) -> CreateOrder:
        """
        Создает новую рекламную кампанию (заказ) и отправляет ее на модерацию.
        Требует `secret_key`.

        Args:
            link: Полная ссылка на ресурс (https://t.me/...).
            ads_type: Тип заказа: 'channel', 'bot' или 'resource'.
            quantity_all: Общее желаемое количество подписчиков.
            name: Название заказа (по умолчанию "Новый заказ").
            is_on: Запустить заказ сразу (1) или поставить на паузу (0).
            quantity_day: Дневной лимит подписчиков.
            price: Базовая цена за подписчика.
            price_premium: Цена за Premium-подписчика (если включен таргетинг).
            bot_token: Токен бота (обязателен, если ads_type='bot').
            to_bot_member: Тип токена (0 - стандартный, 1 - BotMembers).
            track_unsubscriptions: Отслеживать отписки (для каналов).
            is_lite: Плавное распределение (1) или максимально быстро (0).
            sub_speed: Скорость вступлений в час (если is_lite=1).
            user_parameters: Параметры таргетинга (UserParameters или dict).
            forbidden_themes: Список кодов запрещенных тематик.
            order_schedule: Расписание показов (OrderSchedule или dict).

        Returns:
            CreateOrder: Объект с ID созданного заказа.
        """
        if isinstance(user_parameters, UserParameters):
            user_parameters = user_parameters.model_dump(exclude_none=True)
        if isinstance(order_schedule, OrderSchedule):
            order_schedule = order_schedule.model_dump(exclude_none=True)

        payload = {
            "action": "create",
            "link": link,
            "ads_type": ads_type,
            "quantity_all": quantity_all,
            "name": name,
            "is_on": is_on,
            "quantity_day": quantity_day,
            "price": price,
            "price_premium": price_premium,
            "bot_token": bot_token,
            "to_bot_member": to_bot_member,
            "track_unsubscriptions": track_unsubscriptions,
            "is_lite": is_lite,
            "sub_speed": sub_speed,
            "user_parameters": user_parameters,
            "forbidden_themes": forbidden_themes,
            "order_schedule": order_schedule
        }
        
        json_data = {k: v for k, v in payload.items() if v is not None}
        
        return await self._make_request(
            method="POST",
            endpoint="orders",
            response_model=CreateOrder,
            json=json_data,
            key_type=KeyType.SECRET
        )

    async def update_order(
        self,
        order_id: int,
        link: Optional[str] = None,
        name: Optional[str] = None,
        is_on: Optional[int] = None,
        in_archive: Optional[int] = None,
        quantity_all: Optional[int] = None,
        quantity_day: Optional[int] = None,
        price: Optional[float] = None,
        price_premium: Optional[float] = None,
        bot_token: Optional[str] = None,
        to_bot_member: Optional[int] = None,
        track_unsubscriptions: Optional[bool] = None,
        is_lite: Optional[int] = None,
        sub_speed: Optional[int] = None,
        user_parameters: Optional[Union[UserParameters, Dict]] = None,
        forbidden_themes: Optional[List[str]] = None,
        order_schedule: Optional[Union[OrderSchedule, Dict]] = None
    ) -> CreateOrder:
        """
        Обновляет параметры существующего заказа.
        Передавайте только те параметры, которые нужно изменить.
        Требует `secret_key`.

        Args:
            order_id: ID заказа, который нужно изменить.
            link: Новая ссылка (нельзя менять, если уже есть подписчики).
            name: Название заказа.
            is_on: 1 - запустить, 0 - остановить.
            in_archive: 1 - в архив, 0 - из архива.
            quantity_all: Общее желаемое количество подписчиков.
            quantity_day: Дневной лимит подписчиков.
            price: Базовая цена за подписчика.
            price_premium: Цена за Premium-подписчика (если включен таргетинг).
            bot_token: Токен бота (обязателен, если ads_type='bot').
            to_bot_member: Тип токена (0 - стандартный, 1 - BotMembers).
            track_unsubscriptions: Отслеживать отписки (для каналов).
            is_lite: Плавное распределение (1) или максимально быстро (0).
            sub_speed: Скорость вступлений в час (если is_lite=1).
            user_parameters: Параметры таргетинга (UserParameters или dict).
            forbidden_themes: Список кодов запрещенных тематик.
            order_schedule: Расписание показов (OrderSchedule или dict).
        Returns:
            CreateOrder: Результат операции.
        """
        if isinstance(user_parameters, UserParameters):
            user_parameters = user_parameters.model_dump(exclude_none=True)
        if isinstance(order_schedule, OrderSchedule):
            order_schedule = order_schedule.model_dump(exclude_none=True)

        payload = {
            "action": "update",
            "order_id": order_id,
            "link": link,
            "name": name,
            "is_on": is_on,
            "in_archive": in_archive,
            "quantity_all": quantity_all,
            "quantity_day": quantity_day,
            "price": price,
            "price_premium": price_premium,
            "bot_token": bot_token,
            "to_bot_member": to_bot_member,
            "track_unsubscriptions": track_unsubscriptions,
            "is_lite": is_lite,
            "sub_speed": sub_speed,
            "user_parameters": user_parameters,
            "forbidden_themes": forbidden_themes,
            "order_schedule": order_schedule
        }

        json_data = {k: v for k, v in payload.items() if v is not None}

        return await self._make_request(
            method="POST",
            endpoint="orders",
            response_model=CreateOrder,
            json=json_data,
            key_type=KeyType.SECRET
        )

    async def get_order_info(self, order_id: int) -> OrderInfo:
        """
        Получает полную информацию о заказе, включая статус, цены и прогресс.
        Требует `secret_key`.

        Args:
            order_id: ID заказа.

        Returns:
            OrderInfo: Полная информация о заказе.
        """
        payload = {
            "action": "info",
            "order_id": order_id
        }
        
        return await self._make_request(
            method="POST",
            endpoint="orders",
            response_model=OrderInfo,
            json=payload,
            key_type=KeyType.SECRET
        )
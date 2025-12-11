from typing import List, Optional, Literal, Union
from datetime import date, datetime
from .base import MethodMixin
from ..base import KeyType
from ..types.publisher import GetSponsors, Bots, GetUserInfo

class PublisherMethods(MethodMixin):
    async def get_sponsors(
        self,
        chat_id: int,
        user_id: int,
        first_name: Optional[str] = None,
        username: Optional[str] = None,
        language_code: Optional[str] = None,
        is_premium: Optional[bool] = None,
        action: Optional[Literal["subscribe", "newtask", "task"]] = "subscribe",
        max_sponsors: Optional[int] = None,
        get_links: Optional[bool] = None,
        exclude_resource_ids: Optional[List[str]] = None,
        exclude_ads_ids: Optional[List[int]] = None
    ) -> GetSponsors:
        """
        Получает список спонсоров для обязательной подписки (ОП).
        Требует `api_key` (ключ бота).

        Args:
            chat_id: ID чата, откуда идет запрос.
            user_id: ID пользователя Telegram.
            first_name: Имя пользователя (обязательно, если бот добавлен без токена).
            username: Юзернейм пользователя (обязательно, если бот добавлен без токена).
            language_code: Язык пользователя.
            is_premium: Есть ли у пользователя Premium.
            action: Тип действия ('subscribe', 'newtask', 'task').
            max_sponsors: Макс. кол-во спонсоров в ответе.
            get_links: True - получить ссылки, False - пусть сервис сам шлет сообщение.
            exclude_resource_ids: Список ID ресурсов для исключения.
            exclude_ads_ids: Список ID заказов для исключения.

        Returns:
            GetSponsors: Список спонсоров и статус.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
            "first_name": first_name,
            "username": username,
            "language_code": language_code,
            "is_premium": is_premium,
            "action": action,
            "max_sponsors": max_sponsors,
            "get_links": int(get_links) if get_links is not None else None,
            "exclude_resource_ids": exclude_resource_ids,
            "exclude_ads_ids": exclude_ads_ids,
        }

        json_data = {k: v for k, v in payload.items() if v is not None}

        return await self._make_request(
            method="POST",
            endpoint="get-sponsors",
            response_model=GetSponsors,
            json=json_data,
            key_type=KeyType.BOT
        )
    
    async def _bots_action(
        self,
        action: Literal["add", "update, info"],
        bot_token: Optional[str] = None,
        bot_id: Optional[int] = None,
        bot_name: Optional[str] = None,
        bot_nickname: Optional[str] = None,
        time_purge: Optional[int] = None,
        max_sponsors: Optional[int] = None,
        get_links: Optional[bool] = None,
        show_quiz: Optional[bool] = None,
        gender_question: Optional[bool] = None,
        age_question: Optional[bool] = None,
        text_op: Optional[str] = None,
        image_op: Optional[str] = None,
        forbidden_themes: List[str] = None,
        is_on: Optional[bool] = None
    ) -> Bots:
        """Internal helper for bot management."""
        if not any([bot_token, bot_id, bot_name, bot_nickname]):
            raise ValueError("You must provide at least one of bot_token, bot_id, bot_name, bot_nickname")
        payload = {
            "action": action,
            "bot_token": bot_token,
            "bot_id": bot_id,
            "bot_name": bot_name,
            "bot_nickname": bot_nickname,
            "time_purge": time_purge,
            "max_sponsors": max_sponsors,
            "get_links": int(get_links) if get_links is not None else None,
            "show_quiz": int(show_quiz) if show_quiz is not None else None,
            "gender_question": int(gender_question) if gender_question is not None else None,
            "age_question": int(age_question) if age_question is not None else None,
            "text_op": text_op,
            "image_op": image_op,
            "forbidden_themes": forbidden_themes,
            "is_on": int(is_on) if is_on is not None else None
        }
        json_data = {k: v for k, v in payload.items() if v is not None}
        return await self._make_request(
            method="POST",
            endpoint="bots",
            response_model=Bots,
            json=json_data,
            key_type=KeyType.SECRET
        )
    
    async def add_bot(
        self,
        bot_token: Optional[str] = None,
        bot_id: Optional[int] = None,
        bot_name: Optional[str] = None,
        bot_nickname: Optional[str] = None,
        time_purge: Optional[int] = None,
        max_sponsors: Optional[int] = None,
        get_links: Optional[bool] = None,
        show_quiz: Optional[bool] = None,
        gender_question: Optional[bool] = None,
        age_question: Optional[bool] = None,
        text_op: Optional[str] = None,
        image_op: Optional[str] = None,
        forbidden_themes: List[str] = None
    ) -> Bots:
        """
        Регистрирует нового бота в системе.
        Нужно указать либо `bot_token`, либо набор (`bot_id`, `bot_name`, `bot_nickname`).
        Требует `secret_key`.

        Args:
            bot_token: Токен бота от BotFather.
            bot_id: ID бота (если нет токена).
            bot_name: Имя бота (если нет токена).
            bot_nickname: Юзернейм бота без @ (если нет токена).
            time_purge: Время кеширования списка спонсоров (в минутах).
            max_sponsors: Кол-во спонсоров в выдаче.
            get_links: Получать ссылки по API (True) или авто-вывод (False).
            show_quiz: Показывать анкету (пол/возраст).
            text_op: Кастомный текст для блока ОП.
            image_op: URL изображения для блока ОП.
            forbidden_themes: Исключенные тематики рекламы.

        Returns:
            Bots: Результат с API-ключом добавленного бота.
        """
        if not any([bot_token, all([bot_id, bot_name, bot_nickname])]):
            raise ValueError("You must provide at least one of bot_token, bot_id, bot_name, bot_nickname")
        return await self._bots_action(
            action="add",
            bot_token=bot_token,
            bot_id=bot_id,
            bot_name=bot_name,
            bot_nickname=bot_nickname,
            time_purge=time_purge,
            max_sponsors=max_sponsors,
            get_links=int(get_links),
            show_quiz=int(show_quiz),
            gender_question=int(gender_question),
            age_question=int(age_question),
            text_op=text_op,
            image_op=image_op,
            forbidden_themes=forbidden_themes
        )
        
    async def update(
        self,
        bot_token: Optional[str] = None,
        bot_id: int = None,
        bot_name: Optional[str] = None,
        bot_nickname: Optional[str] = None,
        time_purge: Optional[int] = None,
        max_sponsors: Optional[int] = None,
        get_links: Optional[bool] = None,
        show_quiz: Optional[bool] = None,
        gender_question: Optional[bool] = None,
        age_question: Optional[bool] = None,
        text_op: Optional[str] = None,
        image_op: Optional[str] = None,
        forbidden_themes: List[str] = None,
        is_on: Optional[bool] = None
    ) -> Bots:
        """
        Обновляет настройки существующего бота.
        Требует `secret_key`.

        Args:
            bot_token: Токен бота от BotFather.
            bot_id: ID бота, которого нужно обновить.
            bot_name: Имя бота (если нет токена).
            bot_nickname: Юзернейм бота без @ (если нет токена).
            time_purge: Время кеширования списка спонсоров (в минутах).
            max_sponsors: Кол-во спонсоров в выдаче.
            get_links: Получать ссылки по API (True) или авто-вывод (False).
            show_quiz: Показывать анкету (пол/возраст).
            gender_question: Показывать вопрос о поле (True) или нет (False).
            age_question: Показывать вопрос о возрасте (True) или нет (False).
            text_op: Кастомный текст для блока ОП.
            image_op: URL изображения для блока ОП.
            forbidden_themes: Исключенные тематики рекламы.
            is_on: Включить (True) или выключить (False) бота в системе.
        Returns:
            Bots: Результат обновления.
        """
        return await self._bots_action(
            action="update",
            bot_token=bot_token,
            bot_id=bot_id,
            bot_name=bot_name,
            bot_nickname=bot_nickname,
            time_purge=time_purge,
            max_sponsors=max_sponsors,
            get_links=get_links,
            show_quiz=show_quiz,
            gender_question=gender_question,
            age_question=age_question,
            text_op=text_op,
            image_op=image_op,
            forbidden_themes=forbidden_themes,
            is_on=is_on
        )
    
    async def get_bot_info(self, bot_id: int) -> Bots:
        """
        Получает информацию и настройки по указанному боту.
        Требует `secret_key`.

        Args:
            bot_id: ID бота.

        Returns:
            Bots: Информация о боте.
        """
        return await self._bots_action(
            action="info",
            bot_id=bot_id
        )
        
    async def get_user_subscriptions(
        self,
        user_id: int,
        links: Optional[List[str]] = None,
        start_date: Optional[Union[date, datetime]] = None,
        end_date: Optional[Union[date, datetime]] = None
    ) -> GetSponsors:
        """
        Проверяет статус подписки пользователя на ресурсы.
        Требует `api_key` (ключ бота).

        Args:
            user_id: ID пользователя Telegram.
            links: Список ссылок для проверки (опционально).
            start_date: Начальная дата выборки (если links не передан).
            end_date: Конечная дата выборки.

        Returns:
            GetSponsors: Статусы подписок (subscribed/unsubscribed).
        """
        payload = {
            "user_id": user_id,
            "links": links,
            "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
            "end_date": end_date.strftime("%Y-%m-%d") if end_date else None
        }
        json_data = {k: v for k, v in payload.items() if v is not None}
        
        return await self._make_request(
            method="POST",
            endpoint="get-user-subscriptions",
            response_model=GetSponsors,
            json=json_data,
            key_type=KeyType.BOT
        )
    
    async def get_user_info(
        self,
        user_id: int
    ) -> GetUserInfo:
        """
        Получает демографические данные о пользователе (пол, возраст, гео, устройство).
        Требует `api_key` (ключ бота).

        Args:
            user_id: ID пользователя Telegram.

        Returns:
            GetUserInfo: Данные о пользователе.
        """
        return await self._make_request(
            method="POST",
            endpoint="get-user-info",
            response_model=GetUserInfo,
            json={"user_id": user_id},
            key_type=KeyType.BOT
        )
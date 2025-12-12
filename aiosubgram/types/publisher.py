from typing import List, Optional, Literal, Any, Union
from pydantic import model_validator
from .base import SubgramObject

class Sponsor(SubgramObject):
    """
    Объект спонсора в списке для подписки.
    """
    ads_id: str
    """Уникальный ID рекламной кампании."""
    
    link: str
    """Готовая ссылка для подписки/перехода."""
    
    resource_id: Optional[Union[str, int]] = None
    """Уникальный ID ресурса (канала или бота) в Telegram."""
    
    type: Literal["channel", "bot", "smart_link", "resource"]
    """
    Тип ресурса:
    - `channel`: Канал или чат.
    - `bot`: Telegram бот.
    - `smart_link`: Умный редирект. Спонсор определится при открытии ссылки.
    - `resource`: Внешний ресурс (miniapp, сайт) или канал/бот без проверки подписки.
    """
    
    status: Literal["subscribed", "unsubscribed", "notgetted"]
    """
    Текущий статус подписки:
    - `subscribed`: Подписан.
    - `unsubscribed`: Не подписан.
    - `notgetted`: Пользователь был подписан ранее и отписался (не уникальный). 
      Telegram не засчитал вступление. Доступ можно давать, но оплата не начисляется.
    """
    
    available_now: bool
    """Флаг, активен ли спонсор в данный момент. Если False, его не следует показывать."""
    
    button_text: str
    """Рекомендуемый текст для кнопки (например 'Подписаться')."""
    
    resource_logo: Optional[str] = None
    """URL на логотип ресурса."""
    
    resource_name: str
    """Название ресурса (канала, бота)."""

class GetSponsors(SubgramObject):
    """
    Ответ метода get_sponsors.
    """
    status: Literal["ok", "warning", "error"]
    """
    - `ok`: Можно пропускать пользователя (подписан или нет спонсоров).
    - `warning`: Не пропускать. Нужно выполнить действие (подписаться).
    - `error`: Произошла ошибка.
    """
    
    message: Optional[str]
    """Сообщение о статусе или ошибке."""
    
    sponsors: List[Sponsor] = []
    """Список спонсоров для подписки."""
    
    @model_validator(mode='before')
    @classmethod
    def flatten_additional_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            additional = data.get('additional')
            if isinstance(additional, dict):
                if 'sponsors' in additional:
                    data['sponsors'] = additional['sponsors']
        return data

class Bot(SubgramObject):
    """
    Информация о боте (Publisher).
    """
    bot_id: int
    """ID бота."""
    
    bot_name: str
    """Имя бота."""
    
    bot_nickname: str
    """Юзернейм бота (без @)."""
    
    status: Optional[str] = None
    """Статус бота (например, active)."""
    
    note: Optional[Any] = None
    """Примечание."""
    
    is_on: bool
    """Включен (True) или выключен (False) бот в системе."""
    
    profit: Optional[float] = 0.0
    """Общий доход."""
    
    profit_own_orders: Optional[float] = 0.0
    """Доход с собственных заказов."""
    
    api_key: str
    """API ключ бота."""
    
    time_purge: int
    """Время (в минутах), на которое кешируется список спонсоров (5-4320)."""
    
    max_sponsors: int
    """Макс. кол-во спонсоров в выдаче (1-10)."""
    
    get_links: bool
    """Получать ссылки по API (True) или авто-вывод SubGram (False)."""
    
    gender_question: bool
    """Показывать вопрос о поле в анкете."""
    
    age_question: bool
    """Показывать вопрос о возрасте в анкете."""
    
    show_quiz: bool
    """Показывать Web App анкету (пол/возраст)."""
    
    text_op: Optional[str] = None
    """Кастомный текст для блока ОП."""
    
    image_op: Optional[str] = None
    """URL изображения для блока ОП."""
    
    forbidden_themes: List[str] = []
    """Список исключенных тематик рекламы."""

class BotAddResult(SubgramObject):
    api_key: str

class Bots(SubgramObject):
    """Ответ методов управления ботами (/bots)."""
    status: Literal["ok", "warning", "error"]
    message: Optional[str] = None
    result: Optional[Union[Bot, BotAddResult]] = None

class UserInfo(SubgramObject):
    """
    Демографические данные пользователя.
    """
    first_name: str
    """Имя пользователя."""
    
    last_name: Optional[str] = None
    """Фамилия пользователя."""
    
    username: Optional[str] = None
    """Юзернейм (без @)."""
    
    lang_code: str
    """Код языка (ru, en...)."""
    
    age_category: int
    """
    ID возрастной категории:
    0: Не определено, 1: <10, 2: 11-13, 3: 14-15, 4: 16-17, 5: 18-25, 6: >25.
    """
    
    age_category_info: str
    """Текстовое описание возраста (например, '> 25')."""
    
    gender: str
    """Пол: male, female."""
    
    country: str
    """Страна."""
    
    city: str
    """Город."""
    
    device_type: str
    """Тип устройства: mobile, desktop, tablet."""
    
    device_os: str
    """ОС: Android, iOS, Mac OS, Windows."""
    
    ip_address: str
    """IP адрес."""
    
    is_suspicious: bool
    """
    True — подозрение на мультиаккаунт/фрод.
    False — пользователь чист.
    """

class GetUserInfo(SubgramObject):
    """Ответ метода get_user_info."""
    status: Literal["ok", "warning", "error"]
    message: Optional[str] = None
    data: UserInfo = None
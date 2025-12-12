from typing import List, Optional, Literal, Union
from .base import SubgramObject

class BotBalanceInfo(SubgramObject):
    """
    Краткая сводка по боту в ответе баланса.
    """
    bot_id: int
    """ID бота."""
    
    bot_username: str
    """Юзернейм бота."""
    
    total_followers: int
    """Общее количество подписчиков бота (аудитория)."""
    
    revenue: float
    """Текущий доход, накопленный ботом."""

class GetBalance(SubgramObject):
    """Ответ метода get_balance."""
    status: Literal["ok", "warning", "error"]
    code: int
    message: Optional[str] = None
    balance: Optional[float] = None
    """Текущий баланс аккаунта."""
    
    bots_info: Optional[List[BotBalanceInfo]] = None
    """Список ботов с их статистикой."""

class FilterValue(SubgramObject):
    """
    Значение фильтра (страна, язык, тематика и т.д.).
    """
    id: Union[int, str]
    """Уникальный идентификатор (ID страны или строковый код тематики)."""
    
    name: str
    """Название."""
    
    percentage: Optional[float] = None
    """Примерная доля этого параметра среди всех пользователей (%)."""

class AdsFilters(SubgramObject):
    """
    Фильтры, применимые к заказам (Advertiser).
    """
    countries: Optional[List[FilterValue]] = None
    languages: Optional[List[FilterValue]] = None
    cities: Optional[List[FilterValue]] = None
    ages: Optional[List[FilterValue]] = None
    devicestype: Optional[List[FilterValue]] = None
    devicesos: Optional[List[FilterValue]] = None
    forbidden_themes: Optional[List[FilterValue]] = None

class BotsFilters(SubgramObject):
    """
    Фильтры, применимые к настройкам ботов (Publisher).
    """
    forbidden_themes: Optional[List[FilterValue]] = None
    """Тематики рекламы, которые можно запретить."""

class AllFilters(SubgramObject):
    ads: Optional[AdsFilters] = None
    bots: Optional[BotsFilters] = None

class GetFilters(SubgramObject):
    """Ответ метода get_filters."""
    filters: Optional[AllFilters] = None

class LanguageStat(SubgramObject):
    """
    Статистика по языкам (для Advertisers).
    """
    lang: str
    """Код языка (ru, en...)."""
    
    percentage: str
    """Процентное соотношение (строка, например '85.4%')."""

class RequestsStats(SubgramObject):
    """
    Статистика API запросов (для Publishers).
    """
    total_requests: int
    successful_requests: int
    failed_requests: Optional[int] = None

class TableDataItem(SubgramObject):
    """
    Элемент таблицы статистики. 
    Поля зависят от action (source/sponsor) и контекста.
    """
    # Для source (Advertiser) / bots (Publisher)
    bot_id: Optional[int] = None
    bot_nickname: Optional[str] = None
    
    # Общие
    subscribers: Optional[int] = None
    value: Optional[float] = None
    is_excluded: Optional[bool] = None
    
    # Для sponsor (Publisher)
    link: Optional[str] = None
    ads_id: Optional[int] = None
    
    # Расширенная статистика (если были показы своих заказов)
    service_subs: Optional[int] = None
    service_value: Optional[float] = None
    own_subs: Optional[int] = None
    own_value: Optional[float] = None

class StatisticData(SubgramObject):
    """
    Данные статистики (графики, таблицы).
    """
    # Общие данные для графиков
    labels: Optional[List[str]] = None
    """Метки (даты) для оси X."""
    
    subscribers_data: Optional[List[int]] = None
    """Количество подписок по датам."""
    
    value_data: Optional[List[float]] = None
    """Суммы расходов/доходов по датам."""
    
    avg_price_data: Optional[List[float]] = None
    """Средняя цена подписчика по датам."""
    
    total_subscribers: Optional[int] = None
    """Итого подписок за период."""
    
    total_value: Optional[float] = None
    """Итого сумма за период."""
    
    # Табличные данные (action=source/sponsor)
    table_data: Optional[List[TableDataItem]] = None
    
    # Данные для Publisher (action=bots)
    show_extended_table: Optional[bool] = None
    """True, если есть статистика по своим заказам."""
    
    requests_stats: Optional[RequestsStats] = None
    """Статистика запросов к API."""
    
    # Данные для Advertiser (action=ads)
    language_stats: Optional[List[LanguageStat]] = None

class GetStatistic(SubgramObject):
    """Ответ метода get_statistic."""
    status: Optional[Literal["ok", "warning", "error"]] = None
    data: Optional[StatisticData] = None

class ToggleExclusion(SubgramObject):
    """Ответ метода toggle_exclusion."""
    status: Literal["ok", "warning", "error"]
    message: str
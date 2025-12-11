from typing import List, Optional, Literal, Union
from .base import SubgramObject

class BotBalanceInfo(SubgramObject):
    bot_id: int
    bot_username: str
    total_followers: int
    revenue: float

class GetBalance(SubgramObject):
    status: Literal["ok", "warning", "error"]
    code: int
    message: Optional[str] = None
    balance: Optional[float] = None
    bots_info: Optional[List[BotBalanceInfo]] = None

class FilterValue(SubgramObject):
    id: Union[int, str]
    name: str
    percentage: Optional[float] = None

class AdsFilters(SubgramObject):
    countries: Optional[List[FilterValue]] = None
    languages: Optional[List[FilterValue]] = None
    cities: Optional[List[FilterValue]] = None
    ages: Optional[List[FilterValue]] = None
    devicestype: Optional[List[FilterValue]] = None
    devicesos: Optional[List[FilterValue]] = None
    forbidden_themes: Optional[List[FilterValue]] = None

class BotsFilters(SubgramObject):
    forbidden_themes: Optional[List[FilterValue]] = None

class AllFilters(SubgramObject):
    ads: Optional[AdsFilters] = None
    bots: Optional[BotsFilters] = None

class GetFilters(SubgramObject):
    filters: Optional[AllFilters] = None

class LanguageStat(SubgramObject):
    lang: str
    percentage: str

class RequestsStats(SubgramObject):
    total_requests: int
    successful_requests: int
    failed_requests: Optional[int] = None

class TableDataItem(SubgramObject):
    bot_id: Optional[int] = None
    bot_nickname: Optional[str] = None
    subscribers: Optional[int] = None
    value: Optional[float] = None
    is_excluded: Optional[bool] = None
    link: Optional[str] = None
    ads_id: Optional[int] = None
    service_subs: Optional[int] = None
    service_value: Optional[float] = None
    own_subs: Optional[int] = None
    own_value: Optional[float] = None

class StatisticData(SubgramObject):
    labels: Optional[List[str]] = None
    subscribers_data: Optional[List[int]] = None
    value_data: Optional[List[float]] = None
    avg_price_data: Optional[List[float]] = None
    total_subscribers: Optional[int] = None
    total_value: Optional[float] = None
    table_data: Optional[List[TableDataItem]] = None
    show_extended_table: Optional[bool] = None
    requests_stats: Optional[RequestsStats] = None
    language_stats: Optional[List[LanguageStat]] = None

class GetStatistic(SubgramObject):
    status: Optional[Literal["ok", "warning", "error"]] = None
    data: Optional[StatisticData] = None

class ToggleExclusion(SubgramObject):
    status: Literal["ok", "warning", "error"]
    message: str
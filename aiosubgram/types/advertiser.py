from typing import List, Optional, Literal, Union
from datetime import datetime, time
from pydantic import field_serializer, field_validator
from .base import SubgramObject

class UserParameters(SubgramObject):
    """
    Параметры таргетинга для заказа.
    Влияют на итоговую стоимость подписчика (коэффициенты).
    """
    gender: Optional[Literal["male", "female", "all"]] = None
    """Пол аудитории. По умолчанию 'all'."""
    
    only_premium: Optional[int] = None
    """
    Таргетинг по Premium:
    0 - любой (default), 1 - только Premium, 2 - без Premium.
    """
    
    languages: Optional[List[int]] = None
    """
    ID языков (из /filters). 
    По умолчанию [1,2,3,4,5] (RU/UZ/KZ/UA/BY). Null для всех языков.
    """
    
    countries: Optional[List[int]] = None
    """ID стран (из /filters). Коэффициент: x2.5"""
    
    cities: Optional[List[int]] = None
    """ID городов (из /filters). Коэффициент: x2.5"""
    
    devicestype: Optional[List[str]] = None
    """Типы устройств (desktop, mobile). Коэффициент: x1.5"""
    
    devicesos: Optional[List[int]] = None
    """ID операционных систем. Коэффициент: x1.5"""
    
    ages: Optional[List[int]] = None
    """
    ID категорий возраста. 
    Коэффициенты: <10 (x1.2), 11-13 (x1.2), 14-15 (x1.5), 16-17 (x1.5), 18-24 (x2.0), >25 (x2.5).
    """
    
    has_photo: Optional[int] = None
    """Наличие фото (1 - да). Коэффициент: x1.1"""
    
    has_username: Optional[int] = None
    """Наличие юзернейма (1 - да). Коэффициент: x1.1"""
    
    has_bio: Optional[int] = None
    """Наличие Bio (1 - да). Коэффициент: x1.1"""
    
    has_first_name: Optional[int] = None
    """Наличие имени (1 - да). Коэффициент: x1.1"""
    
    has_ru_name: Optional[int] = None
    """Наличие имени на кириллице (1 - да). Коэффициент: x1.1"""
    
    has_fake_check: Optional[int] = None
    """Прохождение анти-фрод проверки (1 - да). Коэффициент: x1.1"""
    
    old_account: Optional[int] = None
    """
    Возраст аккаунта:
    1 (>2 лет, x1.1), 2 (>3 лет, x1.2), 3 (>5 лет, x1.3), 4 (>7 лет, x1.4), 5 (>9 лет, x1.5).
    """

class OrderSchedule(SubgramObject):
    """
    Настройки расписания показов заказа.
    """
    start_datetime: Optional[datetime] = None
    """Отложенный запуск (YYYY-MM-DD HH:MM:SS)."""
    
    start_time: Optional[time] = None
    """Время начала показов ежедневно (HH:MM)."""
    
    end_time: Optional[time] = None
    """Время окончания показов ежедневно (HH:MM)."""
    
    excluded_days: Optional[List[int]] = None
    """Дни недели для исключения (1=Пн, ... 7=Вс)."""

    @field_validator('start_time', 'end_time', mode='before')
    @classmethod
    def validate_time(cls, v: Optional[Union[str, time]]) -> Optional[Union[str, time]]:
        if isinstance(v, str):
            parts = v.split(':')
            if len(parts) > 0 and len(parts[0]) == 1:
                return f"0{v}"
        return v

    @field_serializer('start_datetime')
    def serialize_datetime(self, v: Optional[datetime], _info):
        if v:
            return v.strftime('%Y-%m-%d %H:%M:%S')
        return None

    @field_serializer('start_time', 'end_time')
    def serialize_time(self, v: Optional[time], _info):
        if v:
            return v.strftime('%H:%M')
        return None

class OrderCoefficients(SubgramObject):
    """
    Примененные коэффициенты стоимости к заказу.
    """
    cities: Optional[float] = None
    ages: Optional[float] = None
    has_photo: Optional[float] = None
    total: Optional[float] = None
    """Итоговый множитель цены."""
    
    countries: Optional[float] = None
    devicestype: Optional[float] = None
    devicesos: Optional[float] = None
    has_username: Optional[float] = None
    has_bio: Optional[float] = None
    has_first_name: Optional[float] = None
    has_ru_name: Optional[float] = None
    has_fake_check: Optional[float] = None
    old_account: Optional[float] = None

class CreateOrderResult(SubgramObject):
    order_id: int

class CreateOrder(SubgramObject):
    """Ответ метода create_order / update_order."""
    status: Literal["ok", "warning", "error"]
    code: int
    message: Optional[str] = None
    response: Optional[CreateOrderResult] = None

class OrderInfoData(SubgramObject):
    """
    Полная информация о заказе.
    """
    order_id: int
    
    status: Literal["Moderation", "Processing", "Stopped", "Finished", "Rejected", "Archived"]
    """
    Статус заказа:
    - Moderation: На модерации.
    - Processing: Активен.
    - Stopped: Остановлен вручную.
    - Finished: Выполнен (лимит достигнут).
    - Rejected: Отклонен (см. reason).
    - Archived: В архиве.
    """
    
    reason: Optional[str] = None
    """Причина отклонения (для Rejected)."""
    
    link: str
    name: Optional[str] = None
    ads_type: Literal["channel", "bot", "resource"]
    track_unsubscriptions: Optional[bool] = None
    to_bot_member: Optional[int] = None
    
    quantity_all: int
    """Общее заказанное количество."""
    
    quantity_day: Optional[int] = None
    """Дневной лимит."""
    
    quantity_now: int
    """Текущее количество выполненных подписок."""
    
    remains: int
    """Осталось выполнить."""
    
    is_on: int
    in_archive: int
    
    old_price: float
    """Базовая цена (до коэффициентов)."""
    
    real_price: float
    """Итоговая цена за подписчика."""
    
    is_lite: int
    sub_speed: Optional[int] = None
    user_parameters: Optional[UserParameters] = None
    order_schedule: Optional[OrderSchedule] = None
    coefficients: Optional[OrderCoefficients] = None

class OrderInfo(SubgramObject):
    """Ответ метода get_order_info."""
    status: Literal["ok", "warning", "error"]
    code: int
    message: Optional[str] = None
    response: Optional[OrderInfoData] = None
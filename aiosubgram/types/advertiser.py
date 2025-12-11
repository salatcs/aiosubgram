from typing import List, Optional, Literal, Union
from datetime import datetime, time
from pydantic import field_serializer, field_validator
from .base import SubgramObject

class UserParameters(SubgramObject):
    gender: Optional[Literal["male", "female", "all"]] = None
    only_premium: Optional[int] = None
    languages: Optional[List[int]] = None
    countries: Optional[List[int]] = None
    cities: Optional[List[int]] = None
    devicestype: Optional[List[str]] = None
    devicesos: Optional[List[int]] = None
    ages: Optional[List[int]] = None
    has_photo: Optional[int] = None
    has_username: Optional[int] = None
    has_bio: Optional[int] = None
    has_first_name: Optional[int] = None
    has_ru_name: Optional[int] = None
    has_fake_check: Optional[int] = None
    old_account: Optional[int] = None

class OrderSchedule(SubgramObject):
    start_datetime: Optional[datetime] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    excluded_days: Optional[List[int]] = None

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
    cities: Optional[float] = None
    ages: Optional[float] = None
    has_photo: Optional[float] = None
    total: Optional[float] = None
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
    status: Literal["ok", "warning", "error"]
    code: int
    message: Optional[str] = None
    response: Optional[CreateOrderResult] = None

class OrderInfoData(SubgramObject):
    order_id: int
    status: Literal["Moderation", "Processing", "Stopped", "Finished", "Rejected", "Archived"]
    reason: Optional[str] = None
    link: str
    name: Optional[str] = None
    ads_type: Literal["channel", "bot", "resource"]
    track_unsubscriptions: Optional[bool] = None
    to_bot_member: Optional[int] = None
    quantity_all: int
    quantity_day: Optional[int] = None
    quantity_now: int
    remains: int
    is_on: int
    in_archive: int
    old_price: float
    real_price: float
    is_lite: int
    sub_speed: Optional[int] = None
    user_parameters: Optional[UserParameters] = None
    order_schedule: Optional[OrderSchedule] = None
    coefficients: Optional[OrderCoefficients] = None

class OrderInfo(SubgramObject):
    status: Literal["ok", "warning", "error"]
    code: int
    message: Optional[str] = None
    response: Optional[OrderInfoData] = None
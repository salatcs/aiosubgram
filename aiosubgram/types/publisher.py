from typing import List, Optional, Literal, Any, Union
from pydantic import model_validator
from .base import SubgramObject

class Sponsor(SubgramObject):
    ads_id: str
    link: str
    resource_id: Optional[Union[str, int]] = None
    type: Literal["channel", "bot", "smart_link", "resource"]
    status: Literal["subscribed", "unsubscribed", "notgetted"]
    available_now: bool
    button_text: str
    resource_logo: Optional[str] = None
    resource_name: str

class GetSponsors(SubgramObject):
    status: Literal["ok", "warning", "error"]
    message: Optional[str]
    sponsors: List[Sponsor] = []
    
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
    bot_id: int
    bot_name: str
    bot_nickname: str
    status: Optional[str] = None
    note: Optional[Any] = None
    is_on: bool
    profit: Optional[float] = 0.0
    profit_own_orders: Optional[float] = 0.0
    api_key: str
    time_purge: int
    max_sponsors: int
    get_links: bool
    gender_question: bool
    age_question: bool
    show_quiz: bool
    text_op: Optional[str] = None
    image_op: Optional[str] = None
    forbidden_themes: List[str] = []

class BotAddResult(SubgramObject):
    api_key: str

class Bots(SubgramObject):
    status: Literal["ok", "warning", "error"]
    message: Optional[str] = None
    result: Optional[Union[Bot, BotAddResult]] = None

class UserInfo(SubgramObject):
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    lang_code: str
    age_category: int
    age_category_info: str
    gender: str
    country: str
    city: str
    device_type: str
    device_os: str
    ip_address: str
    is_suspicious: bool

class GetUserInfo(SubgramObject):
    status: Literal["ok", "warning", "error"]
    message: Optional[str] = None
    data: UserInfo = None
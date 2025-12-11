from typing import Optional, Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..client import SubgramClient
from ..types.publisher import GetSponsors

async def create_op_keyboard(
    sponsors_response: Optional[GetSponsors] = None,
    client: Optional[SubgramClient] = None,
    channel_text: str = "➕ Подписаться",
    bot_text: str = "➕ Перейти в бота",
    smart_link_text: str = "➕ Перейти",
    resource_text: str = "➕ Перейти",
    done_button_text: Optional[str] = "✅ Я подписался!",
    **kwargs
) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру (InlineKeyboardMarkup) для aiogram на основе списка спонсоров.
    
    Если `sponsors_response` не передан, функция сама сделает запрос к API через `client`.

    Args:
        sponsors_response: Объект ответа от get_sponsors (если уже есть).
        client: Экземпляр SubgramClient (нужен, если sponsors_response is None).
        channel_text: Текст на кнопке для каналов (можно использовать {name}).
        bot_text: Текст на кнопке для ботов.
        smart_link_text: Текст на кнопке для смарт-ссылок.
        resource_text: Текст на кнопке для внешних ресурсов.
        done_button_text: Текст кнопки проверки подписки (callback_data: "subgram-done").
        **kwargs: Аргументы для get_sponsors (chat_id, user_id и т.д.), если запрос делается внутри.

    Returns:
        InlineKeyboardMarkup: Готовая клавиатура со ссылками на спонсоров.
    """
    if not sponsors_response:
        sponsors_response = await client.get_sponsors(**kwargs)
        
    kb_builder = InlineKeyboardBuilder()
    
    buttons = []
    
    for sponsor in sponsors_response.sponsors:
        if sponsor.status != "unsubscribed":
            continue
        if sponsor.type == "channel":
            buttons.append(
                InlineKeyboardButton(text=channel_text, url=sponsor.link)
            )
        elif sponsor.type == "bot":
            buttons.append(
                InlineKeyboardButton(text=bot_text, url=sponsor.link)
            )
        elif sponsor.type == "smart_link":
            buttons.append(
                InlineKeyboardButton(text=smart_link_text, url=sponsor.link)
            )
        elif sponsor.type == "resource":
            buttons.append(
                InlineKeyboardButton(text=resource_text, url=sponsor.link)
            )
    if buttons:
        kb_builder.row(*buttons)

        if done_button_text:
            kb_builder.row(
                InlineKeyboardButton(text=done_button_text, callback_data="subgram-done")
            )
        return kb_builder.as_markup()
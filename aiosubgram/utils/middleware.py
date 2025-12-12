from types import Optional
from aiogram import BaseMiddleware
from ..client import SubgramClient
from .keyboard import create_op_keyboard

class OPMiddleware(BaseMiddleware):
    def __init__(self, client: SubgramClient, max_sponsors: int = 5,
                 sub_text: str = "Чтобы получить доступ к боту, подпишитесь:",
                 channel_text: str = "➕ Подписаться", bot_text: str = "➕ Перейти в бота",
                 smart_link_text: str = "➕ Перейти", resource_text: str = "➕ Перейти",
                 done_button_text: str = "✅ Я подписался!"):
        """Миддлварь для aiogram, которая добавляет клавиатуру с кнопками подписки на каналы, боты, смарт-ссылки и внешние ресурсы.

        Args:
            client (SubgramClient): Экземпляр SubgramClient.
            max_sponsors (int): Максимальное количество спонсоров. По умолчанию: 5.
            sub_text (str): Текст на кнопке подписки. По умолчанию: "Чтобы получить доступ к боту, подпишитесь:".
            channel_text (str): Текст на кнопке для каналов. По умолчанию: "➕ Подписаться".
            bot_text (str): Текст на кнопке для ботов. По умолчанию: "➕ Перейти в бота".
            smart_link_text (str): Текст на кнопке для смарт-ссылок. По умолчанию: "➕ Перейти".
            resource_text (str): Текст на кнопке для внешних ресурсов. По умолчанию: "➕ Перейти".
            done_button_text (str): Текст на кнопке "Я подписался!". По умолчанию: "✅ Я подписался!"
        """
        self.client = client
        self.max_sponsors = max_sponsors
        self.sub_text = sub_text
        self.channel_text = channel_text
        self.bot_text = bot_text
        self.smart_link_text = smart_link_text
        self.resource_text = resource_text
        self.done_button_text = done_button_text
    async def __call__(self, handler, event, data):
        if not hasattr(event, "from_user"):
            return
        try:
            sponsors_response = await self.client.get_sponsors(
                event.from_user.id,
                event.from_user.id,
                event.from_user.first_name,
                event.from_user.username,
                event.from_user.language_code,
                event.from_user.is_premium,
                max_sponsors=self.max_sponsors
            )
            if sponsors_response.status == "warning":
                keyboard = await create_op_keyboard(
                    sponsors_response,
                    self.client,
                    self.channel_text,
                    self.bot_text,
                    self.smart_link_text,
                    self.resource_text,
                    self.done_button_text
                )
                await event.bot.send_message(event.from_user.id, self.sub_text, reply_markup=keyboard)
                return
            return await handler(event, data)
        except Exception as e:
            print(e)
            return await handler(event, data)
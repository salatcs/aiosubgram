import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties

from aiosubgram import SubgramClient
from aiosubgram.utils.middleware import OPMiddleware

BOT_TOKEN = "..."
SUBGRAM_API_KEY = "..." 

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

subgram = SubgramClient(
    api_key=SUBGRAM_API_KEY
)

dp.message.middleware(
    OPMiddleware(
        client=subgram,
        max_sponsors=5,
        sub_text="🔒 <b>Доступ закрыт!</b>\n\nЧтобы пользоваться ботом, подпишитесь на наших спонсоров:",
        channel_text="📢 Подписаться",
        bot_text="🤖 Запустить бота",
        done_button_text="✅ Я подписался"
    )
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"👋 Привет, {message.from_user.full_name}!\n\nЕсли ты видишь это сообщение, значит ты успешно прошел проверку подписки (ОП).")

@dp.callback_query(F.data == "subgram-done")
async def check_subscription_callback(callback: CallbackQuery):
    try:
        response = await subgram.get_sponsors(
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id,
            first_name=callback.from_user.first_name,
            username=callback.from_user.username,
            language_code=callback.from_user.language_code,
            is_premium=callback.from_user.is_premium
        )

        if response.status == "ok":
            await callback.answer("✅ Подписка подтверждена!")
            try:
                await callback.message.delete()
            except Exception:
                pass
            
            await callback.message.answer(f"🎉 Спасибо за подписку!\nДоступ открыт. Нажмите /start")
        else:
            await callback.answer("❌ Вы подписались не на всех спонсоров!", show_alert=True)
            
            
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        await callback.answer("Произошла ошибка при проверке.", show_alert=True)

async def main() -> None:
    try:
        async with subgram:
            await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
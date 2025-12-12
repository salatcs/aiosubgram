
# 🚀 aiosubgram

![PyPI - Version](https://img.shields.io/pypi/v/aiosubgram?style=flat-square&color=blue)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/github/license/salatcs/aiosubgram?style=flat-square)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-2ca5e0?style=flat-square&logo=telegram)

**aiosubgram** — это современная асинхронная Python библиотека для взаимодействия с API сервиса монетизации [subgram.org](https://subgram.org).

Библиотека полностью покрывает функционал API, поддерживает строгую типизацию (Pydantic) и предоставляет готовые инструменты для легкой интеграции с **aiogram 3.x**.

---

## ✨ Особенности

- ⚡ **Полностью асинхронная** (на базе `aiohttp`).
- 🛡 **Строгая типизация**: Все ответы API валидируются через Pydantic модели.
- 🤖 **Aiogram 3 Integration**: Встроенные Middleware и клавиатуры для реализации ОП (Обязательной Подписки).
- 📦 **Полное покрытие API**: Поддержка всех методов для **Рекламодателей**, **Владельцев ботов (Publisher)** и **Общей статистики**.
- 🛠 **Удобная обработка ошибок**: Понятные исключения для отладки.

---

### Документация

[aiosubgram Docs](https://salatcs.github.io/aiosubgram/)

---

## 📥 Установка

Установите библиотеку через pip:

```bash
pip install aiosubgram
```

---

## 🚀 Быстрый старт

Для начала работы вам понадобятся ключи от Subgram. Их можно найти в личном кабинете.

- **Secret Key**: Для управления заказами и ботами.
- **API Token**: Для просмотра статистики и баланса.
- **API Key (Bot)**: Для проверки подписок конкретного бота.

### Базовый пример (получение баланса)

```python
import asyncio
from aiosubgram import SubgramClient

async def main():
    # Инициализация клиента
    client = SubgramClient(
        api_token="ВАШ_API_TOKEN"
    )

    async with client:
        balance = await client.get_balance()
        print(f"Текущий баланс: {balance.balance}$")
        
        for bot in balance.bots_info:
            print(f"Бот {bot.bot_username}: {bot.revenue}$")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🤖 Интеграция с Aiogram 3

Библиотека предоставляет готовый `Middleware`, который автоматически проверяет подписку пользователя на спонсоров перед обработкой любого сообщения.

### Пример бота с ОП (Обязательной Подпиской)

```python
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiosubgram import SubgramClient
from aiosubgram.utils.middleware import OPMiddleware

# Конфигурация
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
SUBGRAM_API_KEY = "YOUR_SUBGRAM_BOT_API_KEY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация клиента Subgram
subgram = SubgramClient(api_key=SUBGRAM_API_KEY)

# Подключение Middleware
dp.message.middleware(
    OPMiddleware(
        client=subgram,
        max_sponsors=3, # Максимум каналов для подписки
        sub_text="🔒 <b>Доступ закрыт!</b>\nПодпишитесь на спонсоров:",
        done_button_text="✅ Я подписался"
    )
)

@dp.message()
async def echo_handler(message: Message):
    # Этот код выполнится только если пользователь подписан
    await message.answer("🎉 Вы прошли проверку! Бот доступен.")

# Обработчик кнопки "Я подписался"
@dp.callback_query(F.data == "subgram-done")
async def check_sub(callback: CallbackQuery):
    response = await subgram.get_sponsors(
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id
    )
    
    if response.status == "ok":
        await callback.message.delete()
        await callback.message.answer("✅ Спасибо! Доступ открыт.")
    else:
        await callback.answer("❌ Вы подписались не на всех!", show_alert=True)

async def main():
    async with subgram:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📚 Функционал

### 📢 Для Владельцев Ботов (Publisher)

Методы для монетизации вашего бота:

- `get_sponsors(...)` — Получить список каналов для подписки (ОП).
- `add_bot(...)` — Добавить нового бота в систему.
- `update(...)` — Обновить настройки бота.
- `get_bot_info(...)` — Получить информацию о боте.
- `get_user_info(...)` — Получить демографию пользователя.

```python
# Пример получения спонсоров вручную
sponsors = await client.get_sponsors(chat_id=123, user_id=456)
for sponsor in sponsors.sponsors:
    print(f"Нужна подписка на: {sponsor.link}")
```

### 🎯 Для Рекламодателей (Advertiser)

Управление рекламными кампаниями:

- `create_order(...)` — Создать заказ (подписчики в канал/бот).
- `update_order(...)` — Изменить параметры заказа (статус, цена).
- `get_order_info(...)` — Получить статус выполнения.

```python
# Создание заказа на подписчиков
order = await client.create_order(
    link="https://t.me/my_channel",
    ads_type="channel",
    quantity_all=1000,
    price=1.3
)
print(f"Заказ создан: ID {order.response.order_id}")
```

### 📊 Общие методы

- `get_balance()` — Баланс аккаунта.
- `get_statistic(...)` — Детальная статистика доходов/расходов.
- `toggle_exclusion(...)` — Блокировка нежелательных ботов/каналов.

---

## ⚙️ Требования

- Python 3.9+
- aiohttp
- pydantic >= 2.0
- aiogram >= 3.x (опционально, для использования utils)

---

## 🤝 Contributing

Баги и предложения можно отправлять в [Issues](https://github.com/salatcs/aiosubgram/issues). Pull Request'ы приветствуются!

---

## 📄 Лицензия

Проект распространяется под лицензией **MIT**. Подробнее см. в файле [LICENSE](LICENSE).

---

<div align="center">
    <b>Copyright (c) 2025 salatcs</b>
</div>
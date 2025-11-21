import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Получаем токен из переменной окружения (задаётся в Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Кому пересылать сообщения
ADMIN_USERNAME = "Maba_wolf"

# Проверка: если токен не задан — ошибка
if not BOT_TOKEN:
    raise ValueError("❌ Ошибка: BOT_TOKEN не задан. Добавьте его в Environment Variables на Render.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "🍷 Привет! Я — секретарь «Свидетеля Бахуса».\n\n"
        "Напишите ваш вопрос или сообщение — я передам его лично Хозяину."
    )

@dp.message()
async def forward_to_admin(message: types.Message):
    user_info = f"@{message.from_user.username}" if message.from_user.username else f"ID {message.from_user.id}"
    text_to_send = message.text or "<медиафайл или не текстовое сообщение>"

    try:
        # Пересылаем вам
        await bot.send_message(
            chat_id=f"@{ADMIN_USERNAME}",
            text=f"📩 Новое сообщение от {user_info}:\n\n{text_to_send}"
        )
        # Ответ отправителю
        await message.answer("✅ Ваше сообщение передано Свидетелю Бахуса!")
    except Exception as e:
        await message.answer("✅ Прямая связь с владельцем канала - @Maba_wolf.")
        print(f"Ошибка пересылки: {e}")

async def main():
    print("✅ Бот-секретарь запущен и ждёт сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

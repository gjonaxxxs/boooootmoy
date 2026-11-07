import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Фейковый сервер для Render (чтобы не убивал бота) ---
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# --- Твой бот ---
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Не найден токен в переменных окружения!")

bot = Bot(token=TOKEN)
dp = Dispatcher() # <--- ВОТ ЭТОЙ СТРОЧКИ НЕ ХВАТАЛО!

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Услуги", callback_data="services")],
        [InlineKeyboardButton(text="Цены", callback_data="prices")],
        [InlineKeyboardButton(text="Связаться", callback_data="contact")]
    ])

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я демонстрационный бот. Выбери нужный раздел ниже:",
        reply_markup=keyboard
    )

@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    if callback.data == "services":
        await callback.message.answer("🛠 Здесь будет список моих услуг.")
    elif callback.data == "prices":
        await callback.message.answer("💰 Здесь будет прайс-лист.")
    elif callback.data == "contact":
        await callback.message.answer("📞 Свяжитесь со мной: @ваш_никнейм")
    
    await callback.answer()

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

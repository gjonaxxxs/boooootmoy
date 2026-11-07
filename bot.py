import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


import os
from aiogram import Bot, Dispatcher, types

# Render возьмет токен из переменной окружения TOKEN
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Не найден токен в переменных окружения!")

bot = Bot(token=TOKEN)

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем кнопки
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


# Обработка нажатий на кнопки
@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    if callback.data == "services":
        await callback.message.answer("🛠 Здесь будет список моих услуг.")
    elif callback.data == "prices":
        await callback.message.answer("💰 Здесь будет прайс-лист.")
    elif callback.data == "contact":
        await callback.message.answer("📞 Свяжитесь со мной: @ваш_никнейм")

    # Убираем "часики" с кнопки
    await callback.answer()


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

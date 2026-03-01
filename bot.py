from aiogram import Bot, Dispatcher, executor, types

import os
TOKEN = os.getenv("BOT_TOKEN")

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    types.KeyboardButton("ℹ️ Ma'lumot"),
    types.KeyboardButton("📞 Aloqa")
)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! 👋\n"
        "Quyidagi tugmalardan birini tanlang 👇",
        reply_markup=keyboard
    )

@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer(f"Siz yozdingiz: {message.text}")

@dp.message_handler(lambda message: message.text == "ℹ️ Ma'lumot")
async def info_handler(message: types.Message):
    await message.answer(
        "Bu bot Tohirjon tomonidan Python (aiogram) yordamida yaratilgan 🤖"
    )

@dp.message_handler(lambda message: message.text == "📞 Aloqa")
async def contact_handler(message: types.Message):
    await message.answer(
        "Bog'lanish uchun:\nTelegram: @TohirjoYuldoshev\nEmail: tohirjonyuldoshev77@gmail.com"
    )

if __name__ == "__main__":
    executor.start_polling(dp)
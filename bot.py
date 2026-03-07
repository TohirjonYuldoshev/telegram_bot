from aiogram import Bot, Dispatcher, executor, types
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# MENU TUGMALARI
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

btn1 = types.KeyboardButton("📚 Darslar")
btn2 = types.KeyboardButton("❓ Test")
btn3 = types.KeyboardButton("ℹ️ Bot haqida")
btn4 = types.KeyboardButton("📞 Aloqa")

keyboard.add(btn1, btn2)
keyboard.add(btn3, btn4)

# START
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! 👋\nBotga xush kelibsiz!\nQuyidagi tugmalardan birini tanlang 👇",
        reply_markup=keyboard
    )

# DARSLAR
@dp.message_handler(lambda message: message.text == "📚 Darslar")
async def lessons(message: types.Message):
    await message.answer(
        "📚 Bu yerda dasturlash darslari bo'ladi.\n"
        "Hozircha darslar tayyorlanmoqda."
    )

# TEST
@dp.message_handler(lambda message: message.text == "❓ Test")
async def test(message: types.Message):
    await message.answer(
        "❓ Testlar tez orada qo'shiladi."
    )

# BOT HAQIDA
@dp.message_handler(lambda message: message.text == "ℹ️ Bot haqida")
async def about(message: types.Message):
    await message.answer(
        "🤖 Bu bot Tohirjon tomonidan Python (aiogram) yordamida yaratilgan."
    )

# ALOQA
@dp.message_handler(lambda message: message.text == "📞 Aloqa")
async def contact(message: types.Message):
    await message.answer(
        "📞 Bog'lanish:\n"
        "Telegram: @TohirjoYuldoshev\n"
        "Email: tohirjonyuldoshev77@gmail.com"
    )

# BOSHQA XABARLAR
@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer("Men faqat tugmalar bilan ishlayman 🙂")

# BOTNI ISHGA TUSHIRISH
if __name__ == "__main__":
    executor.start_polling(dp)
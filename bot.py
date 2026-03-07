from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 6101353443

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# DATABASE
conn = sqlite3.connect("users.dp")
cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS users(user_id INTEGER) """)
conn.commit()

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

    user_id = message.from_user.id

    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    if data is None:
        cursor.execute("INSERT INTO users VALUES (?)", (user_id,))
        conn.commit()

    await message.answer(
        "Salom! 👋\nBotga xush kelibsiz!",
        reply_markup=keyboard
    )

# DARSLAR
@dp.message_handler(lambda message: message.text == "📚 Darslar")
async def lessons(message: types.Message):
    await message.answer("📚 Darslar tez orada qo‘shiladi.")

# TEST
@dp.message_handler(lambda message: message.text == "❓ Test")
async def test(message: types.Message):
    await message.answer("❓ Testlar tez orada qo‘shiladi.")

# BOT HAQIDA
@dp.message_handler(lambda message: message.text == "ℹ️ Bot haqida")
async def about(message: types.Message):
    await message.answer("🤖 Bu bot Tohirjon tomonidan yaratilgan.")

# ALOQA
@dp.message_handler(lambda message: message.text == "📞 Aloqa")
async def contact(message: types.Message):
    await message.answer("Telegram: @TohirjoYuldoshev")

# ADMIN - USER COUNT
@dp.message_handler(commands=["users"])
async def users_count(message: types.Message):

    if message.from_user.id == ADMIN_ID:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        await message.answer(f"👥 Foydalanuvchilar soni: {len(users)}")

# ADMIN - BROADCAST
@dp.message_handler(commands=["broadcast"])
async def broadcast(message: types.Message):

    if message.from_user.id == ADMIN_ID:

        text = message.get_args()

        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()

        for user in users:
            try:
                await bot.send_message(user[0], text)
            except:
                pass

        await message.answer("📢 Xabar yuborildi!")

# DEFAULT
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Tugmalardan foydalaning 🙂")

if __name__ == "__main__":
    executor.start_polling(dp)
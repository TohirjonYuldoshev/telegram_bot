import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


# Asosiy tugma
main_keyboard = [
    ["🧠 Test"]
]

main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)


# Daraja tugmalari
level_keyboard = [
    ["🟢 Oson"],
    ["🟡 O'rtacha"],
    ["🔴 Qiyin"]
]

level_markup = ReplyKeyboardMarkup(level_keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 👋\nAI test botga xush kelibsiz.\n\nTest boshlash uchun 🧠 Test tugmasini bosing.",
        reply_markup=main_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # Test bosildi
    if text == "🧠 Test":
        await update.message.reply_text(
            "Qaysi fan bo'yicha test kerak? (Masalan: Matematika, Fizika, Ingliz tili)"
        )
        context.user_data["waiting_subject"] = True
        return

    # Fan yozildi
    if context.user_data.get("waiting_subject"):
        context.user_data["subject"] = text
        context.user_data["waiting_subject"] = False
        context.user_data["waiting_level"] = True

        await update.message.reply_text(
            "Darajani tanlang:",
            reply_markup=level_markup
        )
        return

    # Daraja tanlandi
    if context.user_data.get("waiting_level"):

        subject = context.user_data.get("subject")
        level = text

        prompt = f"""
        {subject} fanidan {level} darajadagi bitta test savoli yoz.
        4 ta variant bo'lsin (A, B, C, D).
        Oxirida to'g'ri javobni ham yoz.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        question = response.choices[0].message.content

        await update.message.reply_text(
            question,
            reply_markup=main_markup
        )

        context.user_data["waiting_level"] = False


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")

app.run_polling()

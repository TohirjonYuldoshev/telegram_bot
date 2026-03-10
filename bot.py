from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from config import BOT_TOKEN, ADMIN_ID
from ai import generate_question, explain_answer
from database import save_result, get_top, get_user_stats, get_global_stats


main_keyboard = [["🧠 Test"], ["🏆 Top"], ["📊 Mening statistikam"]]
main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

level_keyboard = [["🟢 Oson"], ["🟡 O'rtacha"], ["🔴 Qiyin"]]
level_markup = ReplyKeyboardMarkup(level_keyboard, resize_keyboard=True)

answer_keyboard = [["A", "B", "C", "D"]]
answer_markup = ReplyKeyboardMarkup(answer_keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Salom 👋\nAI Test Botga xush kelibsiz.\n\n🧠 Test tugmasini bosing.",
        reply_markup=main_markup
    )


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    top = get_top()

    if not top:
        await update.message.reply_text("Hozircha natijalar yo'q.")
        return

    text = "🏆 Eng yaxshi natijalar\n\n"

    for i, row in enumerate(top):

        username = row[0] or "user"
        score = row[1]

        text += f"{i+1}. @{username} — {score}\n"

    await update.message.reply_text(text)


async def my_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    count, best, avg = get_user_stats(user_id)

    if count == 0:
        await update.message.reply_text("Siz hali test ishlamadingiz.")
        return

    text = f"""
📊 Sizning statistikangiz

Ishlangan testlar: {count}
Eng yaxshi natija: {best}
O'rtacha ball: {round(avg,2)}
"""

    await update.message.reply_text(text)


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return

    users, tests, best = get_global_stats()

    text = f"""
📊 Bot statistikasi

👥 Foydalanuvchilar: {users}
🧠 Ishlangan testlar: {tests}
🏆 Eng yaxshi natija: {best}
"""

    await update.message.reply_text(text)


async def send_question(update, context):

    subject = context.user_data["subject"]
    level = context.user_data["level"]

    question, answer = generate_question(subject, level)

    context.user_data["correct_answer"] = answer
    context.user_data["last_question"] = question

    await update.message.reply_text(
        question,
        reply_markup=answer_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "🧠 Test":

        await update.message.reply_text("Qaysi fan?")
        context.user_data["waiting_subject"] = True
        return


    if context.user_data.get("waiting_subject"):

        context.user_data["subject"] = text
        context.user_data["waiting_subject"] = False
        context.user_data["waiting_level"] = True

        await update.message.reply_text(
            "Darajani tanlang:",
            reply_markup=level_markup
        )

        return


    if context.user_data.get("waiting_level"):

        context.user_data["level"] = text
        context.user_data["waiting_level"] = False

        context.user_data["score"] = 0
        context.user_data["question_count"] = 0

        await send_question(update, context)
        return


    if text in ["A","B","C","D"] and context.user_data.get("correct_answer"):

        question = context.user_data["last_question"]

        if text == context.user_data["correct_answer"]:

            context.user_data["score"] += 1
            await update.message.reply_text("✅ To'g'ri!")

        else:

            explanation = explain_answer(question)

            await update.message.reply_text(
                f"❌ Noto'g'ri\n\n🤖 AI tushuntirish:\n{explanation}"
            )


        context.user_data["question_count"] += 1


        if context.user_data["question_count"] >= 10:

            score = context.user_data["score"]

            user_id = update.message.from_user.id
            username = update.message.from_user.username

            save_result(user_id, username, score)

            await update.message.reply_text(
                f"🎉 Test tugadi\n\nNatija: {score}/10",
                reply_markup=main_markup
            )

            return


        await send_question(update, context)
        return


    if text == "🏆 Top":

        await leaderboard(update, context)


    if text == "📊 Mening statistikam":

        await my_stats(update, context)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("top", leaderboard))
app.add_handler(CommandHandler("me", my_stats))
app.add_handler(CommandHandler("stats", admin_stats))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")

app.run_polling()
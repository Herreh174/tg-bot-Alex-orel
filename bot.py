import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq

# Инициализация Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Обработчики команд
async def start(update: Update, context):
    await update.message.reply_text("🤖 Привет! Я бот на Groq (Llama 3 70B). Задай вопрос!")

async def handle_message(update: Update, context):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": update.message.text}],
            model="llama3-70b-8192",
            temperature=0.7,
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

# Запуск бота
def main():
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

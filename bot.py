pip install python-telegram-bot groq


import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq



# Инициализация Groq
client = Groq(api_key=GROQ_API_KEY)

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я Алекс Птица. Решу любой вопрос!")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context):
    user_message = update.message.text
    
    # Отправляем запрос в Groq
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model="llama3-70b-8192",  # Самая мощная модель
        temperature=0.7,  # Контроль "креативности" (0-1)
    )
    
    # Отправляем ответ пользователю
    await update.message.reply_text(response.choices[0].message.content)

# Запуск бота
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()

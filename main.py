import telebot
from telebot import types

bot = telebot.TeleBot('8170370022:AAEITgTDYgoItgTC6VyRXOBv77HAxB8bpz4')

@bot.message_handler(commands=['start'])
def start(message):
    # Имя пользователя для персонализации
    user_name = message.from_user.first_name or "друг"

    # Inline-клавиатура с WebApp
    keyboard = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo("https://mar-egyptian-devices-indiana.trycloudflare.com")  # Ссылка на ваше приложение
    keyboard.add(types.InlineKeyboardButton("Открыть магазин", web_app=web_app))

    # Приветственное сообщение
    text = f"""
Добро пожаловать, {user_name}! 👋

Откройте наш магазин MiniApp, чтобы найти всё необходимое. Удачных покупок!
"""

    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(commands=['id'])
def id(message):
    bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}')


@bot.message_handler()
def info(message):
    bot.send_message(message.chat.id, "Извините, я вас не понимаю. Попробуйте команду /start.")


# Запуск бота
bot.polling()

import telebot, os
from telebot import types
from flask import Flask, send_from_directory
from threading import Thread

app = Flask(__name__, template_folder='.')
bot = telebot.TeleBot('8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8')
URL = "https://microtask-bb30.onrender.com"

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url=URL)))
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url=URL)))
    bot.send_message(message.chat.id, "স্বাগতম! আপনার পছন্দের সার্ভিসে প্রবেশ করুন:", reply_markup=markup)

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

import telebot, os
from telebot import types
from flask import Flask, send_from_directory
from threading import Thread

app = Flask(__name__, template_folder='.')
TOKEN = '8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8'
bot = telebot.TeleBot(TOKEN)
# রেন্ডার সার্ভিসের মূল URL
RENDER_URL = "https://microtask-bb30.onrender.com"

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/earn')
def earn_page():
    return send_from_directory('.', 'earn.html')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # শপিং বাটন: আপনার ব্লগস্পট সাইট
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url="https://ardigitalmart.blogspot.com")))
    # আর্নিং বাটন: আপনার রেন্ডার সার্ভারের /earn পাথ
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url=f"{RENDER_URL}/earn")))
    bot.send_message(message.chat.id, "স্বাগতম! নিচের বাটন থেকে আপনার সার্ভিস সিলেক্ট করুন:", reply_markup=markup)

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

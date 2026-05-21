import telebot, os, json, firebase_admin
from telebot import types
from firebase_admin import credentials, db
from flask import Flask, send_from_directory
from threading import Thread

# রেন্ডার এনভায়রনমেন্ট থেকে কি নেওয়া
cred_json = os.environ.get('FIREBASE_CREDENTIALS')
if cred_json:
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com/'})

app = Flask(__name__, template_folder='.')
bot = telebot.TeleBot('8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8')

@app.route('/')
def home(): return send_from_directory('.', 'index.html')
@app.route('/earn')
def earn(): return send_from_directory('.', 'index.html')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url="https://ardigitalmart.blogspot.com")))
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url="https://microtask-bb30.onrender.com/earn")))
    bot.send_message(message.chat.id, "স্বাগতম! আপনার পছন্দের সার্ভিসটি সিলেক্ট করুন:", reply_markup=markup)

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

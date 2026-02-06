import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask, render_template
import threading
import time

# ফায়ারবেস সেটআপ
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
    })

# আপনার নতুন এপিআই কি
API_TOKEN = '8316197397:AAFJnkVvRsi1wuQXBtifyB9Wc_DRBZILS-8'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url="https://microtask-bb30.onrender.com") 
    markup.add(types.InlineKeyboardButton("💰 ড্যাশবোর্ড", web_app=web_app))
    bot.send_message(message.chat.id, "ইনকাম শুরু করতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

def run_bot():
    bot.remove_webhook()
    time.sleep(2) # Conflict ফিক্স করতে
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

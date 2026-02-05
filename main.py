import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask, render_template
import threading

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
})

API_TOKEN = 'API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    webapp = types.WebAppInfo(url="https://microtask-bb30.onrender.com")
    markup.add(types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=webapp))
    bot.send_message(message.chat.id, "ড্যাশবোর্ড খুলুন", reply_markup=markup)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))

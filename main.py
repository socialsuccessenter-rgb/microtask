import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body { background: #0f172a; color: white; text-align: center; font-family: sans-serif; margin:0; padding: 20px; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; display: block; margin-top: 50px; }
            h1 { color: #38bdf8; font-size: 24px; }
            .balance { font-size: 40px; color: #4ade80; font-weight: bold; margin: 20px 0; }
            .btn { background: #38bdf8; color: #0f172a; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: bold; display: block; width: 100%; border: none; font-size: 18px; }
        </style>
    </head>
    <body onload="window.Telegram.WebApp.expand()">
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার ব্যক্তিগত মিনি অ্যাপ</p>
            <div class="balance">$0.018</div>
            <button class="btn" onclick="alert('কাজ শুরু হচ্ছে...')">কাজ শুরু করুন 💰</button>
        </div>
    </body>
    </html>
    """

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TOKEN = '8316197397:AAE0e7fmbYNCtPv7pBgRk6WI1AktYtvQKrg'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # WebAppInfo সঠিকভাবে ব্যবহারের ফলে এটি সরাসরি ওপেন হবে
    markup.add(types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=URL)))
    bot.send_message(message.chat.id, "সালাম! আপনার ড্যাশবোর্ড প্রস্তুত।", reply_markup=markup)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling()

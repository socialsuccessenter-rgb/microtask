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
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MicroTask V33</title>
        <style>
            body { background: #0f172a; color: white; text-align: center; padding-top: 50px; font-family: sans-serif; }
            .card { background: #1e293b; padding: 25px; border-radius: 15px; border: 1px solid #38bdf8; display: inline-block; }
            h1 { color: #38bdf8; }
            .balance { font-size: 24px; color: #4ade80; margin: 15px 0; }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>MicroTask V33 Dashboard</h1>
            <div class="balance">ব্যালেন্স: $0.018</div>
            <a href="আপনার_মনিট্যাগ_লিংক" class="btn">কাজ শুরু করুন 💰</a>
        </div>
    </body>
    </html>
    """

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # নিশ্চিত করুন এই লিংকটি আপনার রেন্ডার ইউআরএল-এর সাথে মিলছে
    WEB_APP_URL = "https://microtask-bb30.onrender.com"
    btn1 = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=WEB_APP_URL))
    btn2 = types.InlineKeyboardButton("👥 Join Community", url="https://t.me/microtask_earnmoney")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "MicroTask V33-এ স্বাগতম! ড্যাশবোর্ড ওপেন করুন:", reply_markup=markup)

def start_bot():
    bot.remove_webhook()
    bot.infinity_polling(timeout=20)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    start_bot()

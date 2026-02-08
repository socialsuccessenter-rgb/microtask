import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. Setup Flask for the Dashboard
app = Flask('')

@app.route('/')
def home():
    # This HTML is what users see when they click "Open Dashboard"
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 50px 20px; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 1px solid #38bdf8; }
            .btn { background: #38bdf8; color: #0f172a; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>MicroTask V33</h1>
            <p>Welcome to your active dashboard!</p>
            <div style="font-size: 24px; color: #4ade80; margin: 20px 0;">Balance: $0.018</div>
            <a href="YOUR_MONETAG_DIRECT_LINK_HERE" class="btn">START EARNING</a>
        </div>
    </body>
    </html>
    """

def run():
    # Port binding for Render to avoid "Timed Out"
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Setup Telegram Bot
TOKEN = '8316197397:AAFLdurYzD6IaFYKv0xQT1zb7rZKMvX1N7w'
bot = telebot.TeleBot(TOKEN)
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # This button opens the WebApp Dashboard
    web_button = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(web_button)
    
    bot.send_message(message.chat.id, "Welcome! Click below to start.", reply_markup=markup)

def start_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    start_bot()

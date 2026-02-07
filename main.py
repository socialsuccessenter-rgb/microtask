import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server to keep Render happy
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# আপনার বটের টোকেন
TOKEN = '8316197397:AAGdoaHnt8vPBrcytx5fN6jTF3-90R7dliI'
bot = telebot.TeleBot(TOKEN)

# আপনার রেন্ডার ওয়েব অ্যাপ লিংক
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    welcome_text = (
        "🌟 **Your Digital Earning Journey Starts Here!**\n\n"
        "Join **MicroTask V33**, the most modern platform to earn money online by doing simple tasks. 🚀\n\n"
        "Click the button below to unlock your personal dashboard! 🗝️"
    )

    markup = types.InlineKeyboardMarkup()
    dashboard_button = types.InlineKeyboardButton(
        text="🚀 Unlock Dashboard", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    support_button = types.InlineKeyboardButton(
        text="💬 Join Community", 
        url="https://t.me/microtask_earnmoney"
    )
    
    markup.add(dashboard_button)
    markup.add(support_button)

    try:
        bot.send_message(user_id, welcome_text, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

def start_bot():
    print("Bot is starting...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Start the Flask server in a separate thread
    t = Thread(target=run)
    t.start()
    # Start the Bot
    start_bot()

import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask সার্ভার যা রেন্ডারকে 'Live' রাখবে
app = Flask(__name__)

@app.route('/')
def home():
    return "MicroTask V33 is officially LIVE!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# আপনার এপিআই টোকেন
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # ড্যাশবোর্ড লিংক (ব্রাউজারে কাজ করার জন্য)
    dashboard_url = "https://microtask-bb30.onrender.com"
    btn1 = types.InlineKeyboardButton("🚀 Open Dashboard", url=dashboard_url)
    
    # কমিউনিটি বাটন
    btn2 = types.InlineKeyboardButton("👥 Join Community", url="https://t.me/microtask_earnmoney")
    
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id, 
        "সালাম ভাই! আপনার বট এখন পুরোপুরি সচল। নিচের বাটন থেকে ড্যাশবোর্ড দেখুন।", 
        reply_markup=markup
    )

def start_bot():
    # কনফ্লিক্ট দূর করতে আগের সব সেশন ক্লিয়ার করবে
    bot.remove_webhook()
    print("Bot is starting to poll...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    start_bot()

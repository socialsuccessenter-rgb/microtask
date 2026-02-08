import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# রেন্ডারকে লাইভ রাখার জন্য Flask
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

# আপনার সঠিক রেন্ডার ড্যাশবোর্ড লিংক
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    
    # এটি এখন টেলিগ্রামের ভেতরেই ড্যাশবোর্ড ওপেন করবে
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    btn1 = types.InlineKeyboardButton(text="🚀 Open Dashboard", web_app=web_app)
    
    markup.add(btn1)
    
    bot.send_message(
        message.chat.id, 
        "সালাম ভাই! এবার আপনার ড্যাশবোর্ড সরাসরি এখানেই ওপেন হবে। নিচের বাটনে ক্লিক করুন।", 
        reply_markup=markup
    )

def start_bot():
    # কনফ্লিক্ট দূর করতে এই ধাপটি সবচেয়ে জরুরি
    bot.remove_webhook()
    print("Bot is starting...")
    bot.infinity_polling(timeout=20)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    start_bot()

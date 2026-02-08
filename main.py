import telebot
from telebot import types
import os
import time
from flask import Flask
from threading import Thread

# ১. Flask সার্ভার সেটিংস (রেন্ডারকে লাইভ রাখার জন্য)
app = Flask(__name__)

@app.route('/')
def home():
    # এটি আপনার ব্রাউজারে দেখা যাবে (cite: 51472.jpg)
    return "MicroTask V33 is officially LIVE and Running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ২. আপনার টেলিগ্রাম বট সেটিংস
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # ড্যাশবোর্ড বাটন (সরাসরি ইউআরএল হিসেবে দেওয়া হলো যাতে 'Not Found' না আসে)
    dashboard_url = "https://microtask-bb30.onrender.com"
    btn1 = types.InlineKeyboardButton("🚀 Open Dashboard", url=dashboard_url)
    
    # আপনার মনিট্যাগ বা কাজের লিংক
    btn2 = types.InlineKeyboardButton("💰 Start Earning", url="https://t.me/microtask_earnmoney")
    
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id, 
        f"সালাম {message.from_user.first_name}! 👋\nআপনার বট এখন সচল। নিচের বাটন থেকে কাজ শুরু করুন।", 
        reply_markup=markup
    )

# ৩. কনফ্লিক্ট এরর (409) দূর করার জন্য বিশেষ ফাংশন
def start_bot():
    while True:
        try:
            print("Conflict দূর করা হচ্ছে এবং বট চালু হচ্ছে...")
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error: {e}. ৫ সেকেন্ড পর আবার চেষ্টা করা হচ্ছে...")
            time.sleep(5)

if __name__ == "__main__":
    # Flask থ্রেড চালু
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # বট পোলিং চালু
    start_bot()

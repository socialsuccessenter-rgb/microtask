import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ১. ড্যাশবোর্ড ইঞ্জিন (Flask)
app = Flask(__name__)

@app.route('/')
def home():
    # এখানে আপনার সেই সুন্দর ড্যাশবোর্ড ডিজাইন
    return """
    <body style="background:#0f172a;color:white;text-align:center;padding-top:50px;font-family:sans-serif;">
        <div style="border:2px solid #38bdf8;padding:30px;border-radius:20px;display:inline-block;box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <h1 style="color:#38bdf8;">🚀 MicroTask V33</h1>
            <p>আপনার আর্নিং ড্যাশবোর্ড</p>
            <div style="font-size:32px;color:#4ade80;margin:20px 0;font-weight:bold;">Balance: $0.018</div>
            <a href="আপনার_মনিট্যাগ_লিংক" style="background:#38bdf8;color:#0f172a;padding:12px 25px;border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;">Start Working 💰</a>
        </div>
    </body>
    """

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ২. টেলিগ্রাম বট সেটিংস
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # সরাসরি টেলিগ্রামের ভেতর ড্যাশবোর্ড ওপেন হবে
    btn = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=URL))
    markup.add(btn)
    
    # --- এই নিচের লাইনটি আপনি আপনার ইচ্ছামতো বদলাতে পারেন ---
    reply_text = "সালাম ভাই! MicroTask V33 বটে আপনাকে স্বাগতম। নিচে ক্লিক করে আপনার ড্যাশবোর্ড দেখুন।"
    
    bot.send_message(message.chat.id, reply_text, reply_markup=markup)

def start_polling():
    bot.remove_webhook()
    print("বট আবার সচল হয়েছে...")
    bot.infinity_polling()

if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True
    t.start()
    start_polling()

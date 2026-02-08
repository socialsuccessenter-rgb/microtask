import telebot
from telebot import types
from flask import Flask, render_template, make_response
import os

# ১. আপনার বটের টোকেন
TOKEN = '8316197397:AAFNu5QAyc5xOlUUjhfEY-ziySR2FHDtYFc'
bot = telebot.TeleBot(TOKEN)
WEB_APP_URL = "https://microtask-bb30.onrender.com"

# ২. Flask সেটআপ
app = Flask(__name__)

# --- বটের কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    # সরাসরি আপনার ওয়েব অ্যাপ ওপেন করবে
    dashboard_button = types.InlineKeyboardButton(
        text="💰 কাজ শুরু করুন / ড্যাশবোর্ড", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(dashboard_button)
    
    bot.send_message(
        message.chat.id, 
        "স্বাগতম! ড্যাশবোর্ড ওপেন করতে নিচের বাটনে ক্লিক করুন।", 
        reply_markup=markup
    )

# --- Flask এর রুট (যেখানে HTML লোড হবে) ---
@app.route('/')
def index():
    # আপনার অরিজিনাল HTML ফাইলটি 'templates/index.html' হিসেবে থাকতে হবে
    response = make_response(render_template('index.html'))
    
    # সিকিউরিটি হেডার যা টেলিগ্রামে পেজ লোড করতে সাহায্য করবে
    response.headers['Content-Security-Policy'] = "frame-ancestors https://t.me https://web.telegram.org;"
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response

# --- রেন্ডারের জন্য বট এবং সার্ভার ম্যানেজমেন্ট ---
# টেলিগ্রাম বটের জন্য ওয়েব হুক বা থ্রেডিং ঝামেলা এড়াতে রেন্ডারে একটি নির্দিষ্ট রুট ব্যবহার করা হয়
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

if __name__ == "__main__":
    # Render এর দেওয়া পোর্টে রান হবে
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

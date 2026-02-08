import telebot
from telebot import types
from flask import Flask, render_template, make_response
import os

# --- বটের অংশ ---
TOKEN = '8316197397:AAFNu5QAyc5xOlUUjhfEY-ziySR2FHDtYFc'
bot = telebot.TeleBot(TOKEN)
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    # সরাসরি আপনার ওয়েব অ্যাপ ওপেন করবে
    dashboard_button = types.InlineKeyboardButton(
        text="💰 কাজ শুরু করুন / ড্যাশবোর্ড", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(dashboard_button)
    
    bot.send_message(message.chat.id, "স্বাগতম! ড্যাশবোর্ড ওপেন করতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

# --- Flask সার্ভার অংশ ---
app = Flask(__name__)

@app.route('/')
def index():
    # আপনার আগের HTML ফাইলটি (যাতে কোনো পরিবর্তন করেননি)
    # সেটি অবশ্যই 'templates' ফোল্ডারের ভেতর 'index.html' নামে থাকতে হবে।
    response = make_response(render_template('index.html'))
    
    # এই হেডারগুলো মাস্ট, নতুবা টেলিগ্রাম পেজ লোড করবে না
    response.headers['Content-Security-Policy'] = "frame-ancestors https://t.me https://web.telegram.org;"
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response

# রেন্ডারে সার্ভার চালানোর জন্য
if __name__ == "__main__":
    # টেলিগ্রাম বট এবং ফ্ল্যাস্ক আলাদাভাবে চালানো নিরাপদ
    # তবে সিম্পল রাখার জন্য আমরা এখানে ফ্ল্যাস্ক রান করছি
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

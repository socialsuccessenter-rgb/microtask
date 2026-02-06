import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask, render_template
import threading

# main.py এর ফায়ারবেস কানেকশন অংশ
try:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
    })
except Exception as e:
    print(f"Error loading Firebase JSON: {e}")

# ২. সঠিক টেলিগ্রাম বট টোকেন
API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)

# ৩. ফ্লাস্ক ওয়েব সার্ভার
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

# ৪. বট কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    
    markup = types.InlineKeyboardMarkup()
    # আপনার রেন্ডার ইউআরএল
    web_app = types.WebAppInfo(url="https://microtask-bb30.onrender.com") 
    btn = types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(user_id, f"স্বাগতম {name}!\nনিচের বাটন থেকে ইনকাম শুরু করুন।", reply_markup=markup)

def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


import telebot
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask
import threading

# ১. ফায়ারবেস সেটআপ
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
    })

# ২. আপনার নতুন টেলিগ্রাম বট টোকেন
API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    
    # নতুন ইউজার ডাটাবেসে সেভ করা
    user_ref = db.reference(f'users/{user_id}')
    if not user_ref.get():
        user_ref.set({'balance': 0, 'ref_count': 0, 'name': name})
    
    bot.reply_to(message, f"স্বাগতম {name}!\nআপনার নতুন রেফারেল বটটি এখন সচল। ইনকাম শুরু করতে আপনার লিঙ্ক শেয়ার করুন।")

# ৩. রেন্ডার ওয়েব সার্ভার
app = Flask(__name__)

@app.route('/')
def health_check():
    return "New Bot is Running!"

def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

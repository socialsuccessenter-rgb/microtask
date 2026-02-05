import telebot
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask
import threading
import time

# ১. ফায়ারবেস কানেকশন
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://earnemoneybot-8836f-default-rtdb.firebaseio.com'
    })

# ২. টেলিগ্রাম বট সেটআপ
# এখানে আপনার একদম নতুন টোকেনটি বসাবেন
API_TOKEN = '8304215251:AAE8C7uEtHd2LO1l-bHyKPS7CRrINs5OESw' 
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        user_id = str(message.from_user.id)
        name = message.from_user.first_name
        
        bot.reply_to(message, f"স্বাগতম {name}!\nআপনার রেফারেল সিস্টেমটি এখন সচল। ইনকাম শুরু করুন।")
        
        # ডাটাবেসে ইউজার চেক
        user_ref = db.reference(f'users/{user_id}')
        if not user_ref.get():
            user_ref.set({'balance': 0, 'ref_count': 0, 'name': name})
    except Exception as e:
        print(f"Error in start: {e}")

# ৩. ওয়েব সার্ভার (Render-এর জন্য)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Alive and Running!"

def run_bot():
    while True:
        try:
            print("Bot is trying to connect to Telegram...")
            # সেশন ক্লিয়ার করে পোলিং শুরু করা
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

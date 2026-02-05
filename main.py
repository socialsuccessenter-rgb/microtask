import telebot
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask
import threading

# ১. ফায়ারবেস সেটআপ (ভুল এড়াতে ট্রাই-ক্যাপ ব্যবহার করা হয়েছে)
try:
    basedir = os.path.dirname(os.path.abspath(__file__))
    cred_path = os.path.join(basedir, "serviceAccountKey.json")
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
        })
    firebase_connected = True
except Exception as e:
    print(f"Firebase Error: {e}")
    firebase_connected = False

# ২. টেলিগ্রাম বট টোকেন
API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    
    balance = 0
    if firebase_connected:
        try:
            user_ref = db.reference(f'users/{user_id}')
            user_data = user_ref.get()
            if not user_data:
                user_ref.set({'balance': 0, 'name': user_name})
            else:
                balance = user_data.get('balance', 0)
        except:
            pass

    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    
    msg = (f"অভিনন্দন {user_name}! আপনার বটটি এখন পুরোপুরি সচল।\n\n"
           f"💰 আপনার ব্যালেন্স: {balance} টাকা\n"
           f"🔗 রেফার লিঙ্ক: {ref_link}\n\n"
           f"রেফার করে ইনকাম শুরু করুন।")
    bot.reply_to(message, msg)

# ৩. ওয়েব সার্ভার
app = Flask(__name__)
@app.route('/')
def index(): return "Bot is Online!"

def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

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

# ২. টেলিগ্রাম বট টোকেন
API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)

# ৩. স্টার্ট কমান্ড ও রেফারেল লজিক
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    args = message.text.split()
    
    user_ref = db.reference(f'users/{user_id}')
    user_data = user_ref.get()

    # নতুন ইউজার হলে ডাটাবেসে যোগ করা
    if not user_data:
        # যদি কেউ রেফার লিঙ্কে ক্লিক করে আসে
        if len(args) > 1:
            referrer_id = args[1]
            if referrer_id != user_id:
                ref_user = db.reference(f'users/{referrer_id}')
                ref_data = ref_user.get()
                if ref_data:
                    new_balance = ref_data.get('balance', 0) + 10 # প্রতি রেফারে ১০ টাকা
                    ref_user.update({'balance': new_balance})
                    try:
                        bot.send_message(referrer_id, f"অভিনন্দন! আপনার রেফারে {user_name} জয়েন করেছে। আপনি ১০ টাকা পেয়েছেন।")
                    except:
                        pass
        
        user_ref.set({'balance': 0, 'name': user_name})
        user_data = {'balance': 0}

    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    msg = (f"স্বাগতম {user_name}!\n\n"
           f"💰 আপনার ব্যালেন্স: {user_data.get('balance', 0)} টাকা\n"
           f"🔗 আপনার রেফার লিঙ্ক: {ref_link}\n\n"
           f"প্রতিটি সফল রেফারেলের জন্য আপনি ১০ টাকা পাবেন।")
    bot.reply_to(message, msg)

# ৪. ওয়েব সার্ভার (Render-এর জন্য)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is Running Perfectly!"

def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

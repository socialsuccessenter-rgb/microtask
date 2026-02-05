import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask, render_template
import threading

# ১. ফায়ারবেস কানেকশন
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
    })

# ২. টেলিগ্রাম বট টোকেন (আপনার টোকেনটি এখানে বসানো হয়েছে)
API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)

# ৩. ফ্লাস্ক ওয়েব সার্ভার (মিনি অ্যাপ হোস্ট করার জন্য)
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    try:
        # এটি আপনার index.html ফাইলটি লোড করবে
        return render_template('index.html')
    except:
        return "Dashboard file (index.html) not found!"

# ৪. বট কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    
    # মিনি অ্যাপ ওপেন করার বাটন
    markup = types.InlineKeyboardMarkup()
    # আপনার রেন্ডার ইউআরএল ব্যবহার করা হয়েছে
    web_app = types.WebAppInfo(url="https://microtask-bb30.onrender.com") 
    btn = types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(user_id, f"স্বাগতম {name}!\nনিচের বাটন থেকে ড্যাশবোর্ড ওপেন করে ইনকাম শুরু করুন।", reply_markup=markup)

# ৫. বট রান করার ফাংশন
def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

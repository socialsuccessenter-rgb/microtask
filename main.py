import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask, render_template
import threading

# ১. ফায়ারবেস সেটআপ (serviceAccountKey.json ব্যবহার করে)
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
        })
    except Exception as e:
        print(f"Firebase Error: {e}")

# ২. টেলিগ্রাম বট টোকেন
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
        return "Dashboard file (index.html) not found in main folder!"

# ৪. বট কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    args = message.text.split()
    
    user_ref = db.reference(f'users/{user_id}')
    user_data = user_ref.get()

    # যদি নতুন ইউজার হয়, তবে ডাটাবেসে নতুন অ্যাকাউন্ট তৈরি
    if not user_data:
        # রেফারেল সিস্টেম চেক
        if len(args) > 1:
            referrer_id = args[1]
            if referrer_id != user_id:
                ref_user_ref = db.reference(f'users/{referrer_id}')
                ref_user_data = ref_user_ref.get()
                if ref_user_data:
                    # রেফারারের অ্যাকাউন্টে ১০ টাকা বোনাস যোগ
                    new_bal = ref_user_data.get('balance', 0) + 10
                    new_ref_count = ref_user_data.get('ref_count', 0) + 1
                    ref_user_ref.update({
                        'balance': new_bal,
                        'ref_count': new_ref_count
                    })
                    try:
                        bot.send_message(referrer_id, f"✅ অভিনন্দন! আপনার রেফারে {name} জয়েন করেছে।\n💰 বোনাস: ১০ টাকা যোগ হয়েছে।")
                    except:
                        pass
        
        # নতুন ইউজারের তথ্য সেভ করা
        user_ref.set({
            'name': name,
            'balance': 0,
            'ref_count': 0
        })

    # টেলিগ্রাম মিনি অ্যাপ ওপেন করার বাটন
    markup = types.InlineKeyboardMarkup()
    # এখানে আপনার রেন্ডার সার্ভারের লিঙ্কটি দিতে হবে
    web_app = types.WebAppInfo(url="https://microtask-earnmoney.onrender.com") 
    btn = types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=web_app)
    markup.add(btn)
    
    welcome_text = (f"👋 স্বাগতম {name}!\n\n"
                    f"আমাদের আর্নিং অ্যাপে আপনাকে স্বাগতম। "
                    f"নিচের বাটনটি ক্লিক করে আপনার ড্যাশবোর্ড ওপেন করুন এবং ইনকাম শুরু করুন।")
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# ৫. বট এবং সার্ভার একসাথে রান করার ফাংশন
def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # বটের জন্য আলাদা থ্রেড চালানো
    threading.Thread(target=run_bot).start()
    # ওয়েব সার্ভার চালু করা (রেন্ডার পোর্ট ১০০০০ ব্যবহার করে)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

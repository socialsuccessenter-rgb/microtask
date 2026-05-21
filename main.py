import telebot, os, firebase_admin
from telebot import types
from firebase_admin import credentials, db
from flask import Flask, send_from_directory
from threading import Thread

# Firebase ইনিশিয়ালাইজেশন
cred = credentials.Certificate(json.loads(os.environ['FIREBASE_CREDENTIALS']))
firebase_admin.initialize_app(cred, {'databaseURL': 'https://ardigitalmartbot-default-rtdb.asia-southeast1.firebasedatabase.app/'})

app = Flask(__name__, template_folder='.')
bot = telebot.TeleBot('8316197397:AAHEr61mYN9wF5wzGh3SpLbM-UUcGP-TrPc')
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    ref = db.reference(f'users/{user_id}')
    
    # নতুন ইউজার হলে ডাটাবেসে তৈরি করা
    if not ref.get():
        ref.set({'referrals': 0})
        
    # রেফারেল লজিক
    text_parts = message.text.split()
    if len(text_parts) > 1:
        referrer_id = text_parts[1]
        if referrer_id != user_id:
            ref_ref = db.reference(f'users/{referrer_id}/referrals')
            current_refs = ref_ref.get() or 0
            ref_ref.set(current_refs + 1)
            bot.send_message(referrer_id, f"🎊 অভিনন্দন! আপনার একজন নতুন রেফারেল হয়েছে। মোট রেফার: {current_refs + 1}")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 ড্যাশবোর্ড আনলক করুন", web_app=types.WebAppInfo(url=URL)))
    bot.send_message(message.chat.id, "স্বাগতম! ড্যাশবোর্ড অনলক করুন।", reply_markup=markup)

# বাকি Flask এবং Thread কোড একই থাকবে...

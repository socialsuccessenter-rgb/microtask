import telebot, os, firebase_admin, json
from telebot import types
from firebase_admin import credentials, db
from flask import Flask, send_from_directory
from threading import Thread

# Firebase কানেকশন (রেন্ডারে অবশ্যই সঠিক ভেরিয়েবল সেট করবেন)
cred = credentials.Certificate(json.loads(os.environ['FIREBASE_CREDENTIALS']))
firebase_admin.initialize_app(cred, {'databaseURL': 'https://ardigitalmartbot-default-rtdb.asia-southeast1.firebasedatabase.app/'})

app = Flask(__name__, template_folder='.')
# শপিং বোটের টোকেনটি মেইন বোট হিসেবে ব্যবহার করছি
TOKEN = '8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8' 
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    # ডাটাবেসে ইউজার রেজিস্টার ও রেফারেল কাউন্ট
    ref = db.reference(f'users/{user_id}')
    if not ref.get():
        ref.set({'referrals': 0, 'balance': 0})
        
    # রেফারেল ট্র্যাকিং
    text_parts = message.text.split()
    if len(text_parts) > 1:
        referrer_id = text_parts[1]
        if referrer_id != user_id:
            ref_ref = db.reference(f'users/{referrer_id}/referrals')
            current_refs = ref_ref.get() or 0
            ref_ref.set(current_refs + 1)
            # পুরনো বোটের রেফারেল নোটিফিকেশন সিস্টেম
            try:
                bot.send_message(referrer_id, f"🎊 অভিনন্দন! আপনি একটি নতুন রেফারেল পেয়েছেন। মোট রেফার: {current_refs + 1}")
            except: pass

    # মেনু বাটন
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url=URL)),
        types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url=f"{URL}/earn")),
        types.InlineKeyboardButton("💳 MY BALANCE", callback_data='balance')
    )
    
    bot.send_message(message.chat.id, "✨ স্বাগতম! আমাদের সার্ভিস ব্যবহার করতে নিচের যেকোনো বাটনে ক্লিক করুন:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'balance')
def check_balance(call):
    user_id = str(call.from_user.id)
    balance = db.reference(f'users/{user_id}/balance').get() or 0
    bot.answer_callback_query(call.id, f"আপনার বর্তমান ব্যালেন্স: {balance} টাকা", show_alert=True)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))).start()
    bot.infinity_polling()

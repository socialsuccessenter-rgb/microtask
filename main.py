import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask
import threading

# ফায়ারবেস সেটআপ
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'})

API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)

# প্রধান মেনু বাটন
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('🖥 অ্যাড টাস্ক')
    item2 = types.KeyboardButton('💰 ব্যালেন্স')
    item3 = types.KeyboardButton('📢 সোশাল টাস্ক')
    item4 = types.KeyboardButton('🔗 রেফার')
    markup.add(item1, item2, item3, item4)
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"👋 স্বাগতম {name}!\nআপনার ড্যাশবোর্ড থেকে কাজ শুরু করুন।", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = str(message.from_user.id)
    
    if message.text == '🖥 অ্যাড টাস্ক':
        # এখানে ভিডিও অ্যাডের মতো ইনলাইন বাটন
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📺 ভিডিও অ্যাড (১)", url="https://youtube.com/yourchannel")
        markup.add(btn)
        bot.send_message(message.chat.id, "নিচের ভিডিওটি ৩০ সেকেন্ড দেখুন এবং আয় করুন:", reply_markup=markup)

    elif message.text == '📢 সোশাল টাস্ক':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("🔵 ফেসবুক পেজ ফলো করুন", url="https://facebook.com/yourpage")
        btn2 = types.InlineKeyboardButton("🔴 ইউটিউব সাবস্ক্রাইব করুন", url="https://youtube.com/yourchannel")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "আমাদের সোশাল মিডিয়া টাস্কগুলো সম্পন্ন করুন:", reply_markup=markup)

    elif message.text == '💰 ব্যালেন্স':
        user_ref = db.reference(f'users/{user_id}')
        data = user_ref.get() or {'balance': 0}
        bot.reply_to(message, f"💵 আপনার বর্তমান ব্যালেন্স: {data.get('balance', 0)} টাকা")

    elif message.text == '🔗 রেফার':
        ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        bot.send_message(message.chat.id, f"🔗 আপনার রেফার লিঙ্ক:\n{ref_link}\n\nপ্রতিটি সফল রেফারে পাবেন ১০ টাকা!")

# রেন্ডার সার্ভার (আগের মতোই থাকবে)
app = Flask(__name__)
@app.route('/')
def index(): return "Task Bot is Running!"

def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

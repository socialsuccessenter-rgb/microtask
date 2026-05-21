import telebot, os, json, firebase_admin
from telebot import types
from firebase_admin import credentials, db
from flask import Flask, send_from_directory
from threading import Thread

# Firebase কনফিগারেশন
cred_json = os.environ.get('FIREBASE_CREDENTIALS')
if cred_json and not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com/'})

app = Flask(__name__, template_folder='.')
bot = telebot.TeleBot('8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8')
CHANNEL_ID = "@microtask_earnmoney"

@app.route('/')
def home(): return send_from_directory('.', 'index.html')
@app.route('/earn')
def earn(): return send_from_directory('.', 'index.html')

@bot.message_handler(commands=['start'])
def start(message):
    # ইউজারকে ডাটাবেসে সেভ করা
    try:
        user_ref = db.reference(f'users/{message.chat.id}')
        user_ref.set({'username': message.chat.username or "No Username", 'first_name': message.chat.first_name})
    except:
        pass

    # চ্যানেল চেক
    try:
        member = bot.get_chat_member(CHANNEL_ID, message.chat.id)
        if member.status in ['member', 'administrator', 'creator']:
            send_shop_menu(message.chat.id)
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 চ্যানেল জয়েন করুন", url="https://t.me/microtask_earnmoney"))
            markup.add(types.InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="verify"))
            bot.send_message(message.chat.id, "কাজ শুরু করতে আগে আমাদের চ্যানেলে জয়েন করুন:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, "বোটটিকে চ্যানেলের এডমিন করুন!")

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    try:
        member = bot.get_chat_member(CHANNEL_ID, call.message.chat.id)
        if member.status in ['member', 'administrator', 'creator']:
            bot.answer_callback_query(call.id, "ভেরিফাইড!")
            send_shop_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "আপনি এখনো জয়েন করেননি!", show_alert=True)
    except:
        bot.answer_callback_query(call.id, "এরর হয়েছে, আবার চেষ্টা করুন।", show_alert=True)

def send_shop_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url="https://ardigitalmart.blogspot.com")))
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url="https://microtask-bb30.onrender.com/earn")))
    bot.send_message(chat_id, "স্বাগতম! আপনার পছন্দের সার্ভিসটি সিলেক্ট করুন:", reply_markup=markup)

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

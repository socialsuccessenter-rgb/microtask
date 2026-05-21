import telebot, os, json, firebase_admin
from telebot import types
from firebase_admin import credentials, db
from flask import Flask, send_from_directory
from threading import Thread

# Firebase কনফিগ (রেন্ডারে Environment variable চেক করুন)
cred_json = os.environ.get('FIREBASE_CREDENTIALS')
if cred_json:
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com/'})

app = Flask(__name__, template_folder='.')
bot = telebot.TeleBot('8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8')
CHANNEL_ID = "@microtask_earnmoney" # আপনার চ্যানেলের ইউজারনেম

@app.route('/')
def home(): return send_from_directory('.', 'index.html')

@bot.message_handler(commands=['start'])
def start(message):
    try:
        # চ্যানেল চেক
        status = bot.get_chat_member(CHANNEL_ID, message.chat.id).status
        if status in ['member', 'administrator', 'creator']:
            show_main_menu(message.chat.id)
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 চ্যানেল জয়েন করুন", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}"))
            markup.add(types.InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="verify"))
            bot.send_message(message.chat.id, "কাজ শুরু করতে আগে আমাদের চ্যানেলে জয়েন করুন:", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "বোটটি চ্যানেলের এডমিন করা আছে কি? চ্যানেল আইডি চেক করুন।")

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    status = bot.get_chat_member(CHANNEL_ID, call.message.chat.id).status
    if status in ['member', 'administrator', 'creator']:
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "আপনি এখনো জয়েন করেননি!", show_alert=True)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    # এখানে ব্লগস্পটের বদলে index.html এ রিডাইরেক্ট হবে
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url="https://microtask-bb30.onrender.com/")))
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url="https://microtask-bb30.onrender.com/")))
    bot.send_message(chat_id, "স্বাগতম! আপনার পছন্দের সার্ভিসটি সিলেক্ট করুন:", reply_markup=markup)

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

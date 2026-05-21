import telebot, os, json, firebase_admin
from telebot import types
from firebase_admin import credentials, db
from flask import Flask, send_from_directory
from threading import Thread

# Firebase কনফিগারেশন (রেন্ডার এনভায়রনমেন্ট ভেরিয়েবল থেকে)
cred_json = os.environ.get('FIREBASE_CREDENTIALS')
if cred_json:
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com/'})

app = Flask(__name__, template_folder='.')
TOKEN = '8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"
CHANNEL_ID = "@microtask_earnmoney" # আপনার চ্যানেলের ইউজারনেম

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/earn')
def earn_page():
    return send_from_directory('.', 'index.html')

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if is_subscribed(message.chat.id):
        show_main_menu(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 চ্যানেল জয়েন করুন", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}"))
        markup.add(types.InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="verify"))
        bot.send_message(message.chat.id, "কাজ শুরু করার আগে আমাদের চ্যানেলে জয়েন করুন:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if is_subscribed(call.message.chat.id):
        bot.answer_callback_query(call.id, "ভেরিফাইড! স্বাগতম।")
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "আপনি এখনো জয়েন করেননি!", show_alert=True)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url="https://ardigitalmart.blogspot.com")))
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url=f"{URL}/earn")))
    bot.send_message(chat_id, "স্বাগতম! আপনার পছন্দের সার্ভিসটি সিলেক্ট করুন:", reply_markup=markup)

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

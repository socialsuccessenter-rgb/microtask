import telebot, os, json
from telebot import types
from flask import Flask, send_from_directory
from threading import Thread

app = Flask(__name__, template_folder='.')
bot = telebot.TeleBot('8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8')
CHANNEL_ID = "@microtask_earnmoney"

@app.route('/')
def home(): return send_from_directory('.', 'index.html')
@app.route('/earn')
def earn(): return send_from_directory('.', 'index.html')

# ১. Start কমান্ড এবং চ্যানেল চেক
@bot.message_handler(commands=['start'])
def start(message):
    try:
        user_id = message.chat.id
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            send_shop_menu(user_id)
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 চ্যানেল জয়েন করুন", url="https://t.me/microtask_earnmoney"))
            markup.add(types.InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="verify"))
            bot.send_message(user_id, "কাজ শুরু করতে আগে আমাদের চ্যানেলে জয়েন করুন:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, "বোটটি চ্যানেলের এডমিন করা আছে কি না নিশ্চিত করুন।")

# ২. ভেরিফিকেশন চেক
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    member = bot.get_chat_member(CHANNEL_ID, call.message.chat.id)
    if member.status in ['member', 'administrator', 'creator']:
        bot.answer_callback_query(call.id, "ভেরিফাইড!")
        send_shop_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "আপনি এখনো জয়েন করেননি!", show_alert=True)

# ৩. মেইন মেনু বাটন
def send_shop_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url="https://ardigitalmart.blogspot.com")))
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url="https://microtask-bb30.onrender.com/earn")))
    bot.send_message(chat_id, "স্বাগতম! আপনার পছন্দের সার্ভিসটি সিলেক্ট করুন:", reply_markup=markup)

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

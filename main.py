import telebot, os, json
from telebot import types
from flask import Flask, send_from_directory
from threading import Thread

app = Flask(__name__, template_folder='.')
bot = telebot.TeleBot('8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8')
CHANNEL_ID = "@microtask_earnmoney" 

@app.route('/')
def home(): return send_from_directory('.', 'index.html')

@bot.message_handler(commands=['start'])
def start(message):
    try:
        # চ্যানেল মেম্বারশিপ চেক
        member = bot.get_chat_member(CHANNEL_ID, message.chat.id)
        if member.status in ['member', 'administrator', 'creator']:
            send_shop_menu(message.chat.id)
        else:
            # জয়েন না করলে বাটন দেখাবে
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 চ্যানেল জয়েন করুন", url="https://t.me/microtask_earnmoney"))
            markup.add(types.InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="verify"))
            bot.send_message(message.chat.id, "কাজ শুরু করতে আগে আমাদের চ্যানেলে জয়েন করুন:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, "চ্যানেল আইডি ভুল বা বোট এডমিন নেই!")

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    member = bot.get_chat_member(CHANNEL_ID, call.message.chat.id)
    if member.status in ['member', 'administrator', 'creator']:
        bot.answer_callback_query(call.id, "ভেরিফাইড!")
        send_shop_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "আপনি এখনো জয়েন করেননি!", show_alert=True)

def send_shop_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    # শপিং এবং আর্নিং বাটন
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url="https://ardigitalmart.blogspot.com")))
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url="https://microtask-bb30.onrender.com/")))
    bot.send_message(chat_id, "স্বাগতম! নিচে আপনার পছন্দের অপশনগুলো দেওয়া হলো:", reply_markup=markup)

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()

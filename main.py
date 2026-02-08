import telebot
from telebot import types
import os
from flask import Flask, send_from_directory
from threading import Thread

app = Flask(__name__, template_folder='.')

# রেফারেল ডাটা মনে রাখার জন্য
user_data = {} 

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TOKEN = '8316197397:AAHEr61mYN9wF5wzGh3SpLbM-UUcGP-TrPc'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    
    if user_id not in user_data:
        user_data[user_id] = 0

    # রেফারেল লজিক
    text_parts = message.text.split()
    if len(text_parts) > 1:
        referrer_id = text_parts[1]
        if referrer_id in user_data and referrer_id != user_id:
            user_data[referrer_id] += 1
            bot.send_message(referrer_id, f"🎊 অভিনন্দন! আপনার একজন নতুন রেফারেল হয়েছে। মোট রেফার: {user_data[referrer_id]}")

    # আপনার সেই আগের সুন্দর রিপ্লাই মেসেজ যা ভিডিওতে ছিল
    welcome_text = (
        "মাইক্রোটাস্কে আপনাকে স্বাগতম। 🎉\n"
        "হাতে থাকা স্মার্ট ফোনসহ সকল ডিভাইস দিয়ে ছোটছোট কাজ করে টাকা ইনকাম করতে "
        "নিচের বাটনে ক্লিক করে আপনার Dashboard আনলক 🔐 করুন। মনে রাখবেন এই সাইট "
        "২৪ ঘন্টার মধ্যে ১০০% 💯 পেমেন্ট করে। আমাদের সাথে থাকার জন্য ধন্যবাদ। 💐"
    )

    markup = types.InlineKeyboardMarkup()
    # আপনার সেই রকেট ওয়ালা বাটন
    markup.add(types.InlineKeyboardButton("🚀 ড্যাশবোর্ড অনলক করুন", web_app=types.WebAppInfo(url=URL)))
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling()

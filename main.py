import telebot
from telebot import types
from flask import Flask, render_template
import threading
import os
import time

# ১. আপনার নতুন এপিআই কি
API_TOKEN = '8316197397:AAFJnkVvRsi1wuQXBtifyB9Wc_DRBZILS-8'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    
    # ইনলাইন বাটন তৈরি
    markup = types.InlineKeyboardMarkup()
    
    # আপনার রেন্ডার ইউআরএল (এখানে id পাস করা হচ্ছে যাতে ওয়েব অ্যাপ ইউজারকে চিনতে পারে)
    web_url = f"https://microtask-bb30.onrender.com?id={user_id}"
    web_app = types.WebAppInfo(url=web_url)
    
    markup.add(types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=web_app))
    
    # স্বাগতম মেসেজ
    bot.send_message(
        message.chat.id, 
        "স্বাগতম! ইনকাম শুরু করতে নিচের বাটনে ক্লিক করুন।\n\nমিনিমাম উইথড্র: ৭০০৳\nপ্রয়োজনীয় রেফার: ১০টি", 
        reply_markup=markup
    )

def run_bot():
    # Conflict এরর এড়াতে রিসেট
    bot.remove_webhook()
    time.sleep(1)
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # বট এবং ফ্লাস্ক সার্ভার একসাথে চালানো
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

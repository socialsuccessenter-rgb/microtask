import telebot
from telebot import types
from flask import Flask, render_template
import threading
import os
import time

API_TOKEN = '8316197397:AAEAa8C8mzFW3beQSez9wN-TXUHkGrlLi0Q'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    
    # ইউআরএল-এর শেষে ?v=999 যোগ করা হয়েছে ক্যাশ ফিক্স করার জন্য
    web_url = f"https://microtask-bb30.onrender.com?id={user_id}&v=999"
    web_app = types.WebAppInfo(url=web_url)
    
    markup.add(types.InlineKeyboardButton("💰 ড্যাশবোর্ড ওপেন করুন", web_app=web_app))
    
    bot.send_message(
        message.chat.id, 
        "আপনার ড্যাশবোর্ড আপডেট করা হয়েছে।\n\n🔹 মিনিমাম উইথড্র: ৭০০৳\n🔹 রেফার প্রয়োজন: ১০টি\n\nনিচের বাটনে ক্লিক করুন।", 
        reply_markup=markup
    )

def run_bot():
    bot.remove_webhook()
    time.sleep(2)
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))


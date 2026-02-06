import telebot
import time
from flask import Flask, render_template
import threading
import os

API_TOKEN = '8316197397:AAFJnkVvRsi1wuQXBtifyB9Wc_DRBZILS-8'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = telebot.types.InlineKeyboardMarkup()
    # এখানে আপনার সঠিক রেন্ডার ইউআরএল দিন
    web_app = telebot.types.WebAppInfo(url=f"https://microtask-bb30.onrender.com?id={user_id}")
    markup.add(telebot.types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=web_app))
    bot.send_message(message.chat.id, "স্বাগতম! কাজ শুরু করতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

def run_bot():
    # কনফ্লিক্ট এরর (409) ফিক্স করার জন্য এটি খুব গুরুত্বপূর্ণ
    bot.remove_webhook()
    time.sleep(2)
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

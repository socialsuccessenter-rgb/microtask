import telebot
import os
from flask import Flask
import threading

# ১. এখানে আপনার BotFather থেকে পাওয়া একদম নতুন টোকেনটি বসান
API_TOKEN = 'আপনার_নতুন_টোকেন_এখানে'
bot = telebot.TeleBot(API_TOKEN)

# ২. সাধারণ রেসপন্স চেক
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "আলহামদুলিল্লাহ! আপনার বট এখন সচল হয়েছে।")

# ৩. রেন্ডারের জন্য ফ্লাস্ক সার্ভার
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is Online!"

def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # বটকে আলাদা করে চালানো
    threading.Thread(target=run_bot).start()
    # সার্ভার পোর্ট সেট করা
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

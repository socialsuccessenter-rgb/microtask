import telebot
import os
from flask import Flask
import threading

# এখানে নতুন টোকেনটি বসান
API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ভাই, অবশেষে আমি কাজ করছি! অভিনন্দন।")

@app.route('/')
def index(): return "Bot is Online"

def run():
    bot.remove_webhook() # পুরনো জট কাটানোর জন্য
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

import telebot
import os
from flask import Flask
import threading

# এখানে আপনার একদম নতুন বটের টোকেনটি বসান
API_TOKEN = 'আপনার_নতুন_বট_টোকেন_এখানে'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "আলহামদুলিল্লাহ! আপনার নতুন বটটি এখন কাজ করছে।")

app = Flask(__name__)

@app.route('/')
def index():
    return "New Bot is Online!"

def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

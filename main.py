import telebot
import os
from flask import Flask
import threading

# আপনার নতুন টোকেন
API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is Online and Ready!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "আলহামদুলিল্লাহ! আপনার নতুন বট এখন সফলভাবে কাজ করছে।")

def run():
    bot.remove_webhook()
    print("Bot is starting to poll...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

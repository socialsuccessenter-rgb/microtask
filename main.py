import telebot
from telebot import types
import os
from flask import Flask, send_from_directory
from threading import Thread

# এখানে '.' দেওয়ার মানে হলো সে একই জায়গায় ফাইলটি খুঁজবে
app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    # সরাসরি আপনার আপলোড করা index.html ফাইলটি ওপেন করবে
    return send_from_directory('.', 'index.html')

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# আপনার নতুন টোকেন
TOKEN = '8316197397:AAHEr61mYN9wF5wzGh3SpLbM-UUcGP-TrPc'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 ড্যাশবোর্ড অনলক করুন", web_app=types.WebAppInfo(url=URL)))
    bot.send_message(message.chat.id, "সালাম! আপনার নিজের তৈরি ড্যাশবোর্ডটি এখন প্রস্তুত।", reply_markup=markup)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling()

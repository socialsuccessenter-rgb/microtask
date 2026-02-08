import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# আপনার সচল এপিআই টোকেন
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌟 **MicroTask V33-এ স্বাগতম!**\n\n"
        "সহজ কাজ সম্পন্ন করে ঘরে বসেই ইনকাম করুন। আপনার ড্যাশবোর্ড এবং কাজের লিংক নিচে দেওয়া হলো।"
    )

    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # ব্রাউজারে কাজ করা ড্যাশবোর্ড লিংক
    dashboard_button = types.InlineKeyboardButton(
        text="🚀 Open Dashboard (External)", 
        url="https://microtask-bb30.onrender.com"
    )
    
    # মনিট্যাগ ডিরেক্ট লিংক (সরাসরি কাজ করার জন্য)
    task_button = types.InlineKeyboardButton(
        text="💰 Start Earning Now", 
        url="আপনার_মনিট্যাগ_ডিরেক্ট_লিংক_এখানে"
    )
    
    # কমিউনিটি বাটন
    support_button = types.InlineKeyboardButton(
        text="💬 Join Community", 
        url="https://t.me/microtask_earnmoney"
    )
    
    markup.add(dashboard_button, task_button, support_button)

    try:
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

def start_bot():
    bot.remove_webhook()
    bot.infinity_polling(timeout=20)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    start_bot()

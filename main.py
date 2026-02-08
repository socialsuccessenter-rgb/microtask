import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server setup
app = Flask(__name__)

@app.route('/')
def home():
    # এটি নিশ্চিত করবে যে সার্ভারটি সচল আছে
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
    
    # ব্রাউজারে আলাদাভাবে ড্যাশবোর্ড ওপেন করার লিংক
    dashboard_button = types.InlineKeyboardButton(
        text="🚀 Open Dashboard", 
        url="https://microtask-bb30.onrender.com"
    )
    
    # আপনার মনিট্যাগ ডিরেক্ট লিংক এখানে বসান
    task_button = types.InlineKeyboardButton(
        text="💰 Start Task & Earn", 
        url="https://www.highrevenuegate.com/example_link" 
    )
    
    # টেলিগ্রাম কমিউনিটি লিংক
    support_button = types.InlineKeyboardButton(
        text="💬 Join Community", 
        url="https://t.me/microtask_earnmoney"
    )
    
    markup.add(dashboard_button, task_button, support_button)

    try:
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(f"Error sending message: {e}")

def start_bot():
    print("Bot is starting...")
    # কোনো সেশন আটকে থাকলে তা ক্লিয়ার করবে
    bot.remove_webhook()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

if __name__ == "__main__":
    # Flask সার্ভার চালু করা হচ্ছে
    t = Thread(target=run)
    t.daemon = True
    t.start()
    # বট পোলিং চালু করা হচ্ছে
    start_bot()

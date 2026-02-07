import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server to keep Render happy
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# আপনার বটের টোকেন
TOKEN = '8316197397:AAFLdurYzD6IaFYKv0xQT1zb7rZKMvX1N7w'
bot = telebot.TeleBot(TOKEN)

# আপনার রেন্ডার ওয়েব অ্যাপ লিংক
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    welcome_text = (
        "🌟 **আপনার ডিজিটাল আয়ের নতুন যাত্রা শুরু হোক এখানে!**\n\n"
        "সবচেয়ে সহজ এবং আধুনিক পদ্ধতিতে ঘরে বসে কাজ করার সুযোগ নিয়ে এলো **MicroTask V33**। 🚀\n\n"
        "প্রতিটি সেকেন্ডকে কাজে লাগিয়ে নিজেকে বদলে ফেলার সময় এখন। আমাদের বিশেষ ইন্টারফেস আপনার কাজের অভিজ্ঞতাকে করবে আরও আনন্দদায়ক। ✨\n\n"
        "নিচের ম্যাজিক বাটনে ক্লিক করে আপনার ব্যক্তিগত ড্যাশবোর্ডটি আনলক করুন! 🗝️"
    )

    markup = types.InlineKeyboardMarkup()
    dashboard_button = types.InlineKeyboardButton(
        text="🚀 Unlock Dashboard", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    support_button = types.InlineKeyboardButton(
        text="💬 Join Community", 
        url="https://t.me/microtask_earnmoney"
    )
    
    markup.add(dashboard_button)
    markup.add(support_button)

    try:
        bot.send_message(user_id, welcome_text, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

def start_bot():
    print("Bot is starting...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Start the Flask server in a separate thread
    t = Thread(target=run)
    t.start()
    # Start the Bot
    start_bot()


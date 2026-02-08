import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server configuration
app = Flask(__name__)

@app.route('/')
def home():
    # ড্যাশবোর্ড যেন কালো না দেখায় তার জন্য এই HTML ডিজাইন
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MicroTask V33 Dashboard</title>
        <style>
            body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 40px 20px; }
            .card { background: #1e293b; padding: 25px; border-radius: 15px; border: 1px solid #38bdf8; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
            h1 { color: #38bdf8; }
            .balance { font-size: 22px; color: #4ade80; margin: 15px 0; }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>MicroTask V33</h1>
            <p>আপনার আর্নিং পোর্টালে স্বাগতম!</p>
            <div class="balance">বর্তমান ব্যালেন্স: $0.018</div>
            <a href="আপনার_মনিট্যাগ_ডিরেক্ট_লিংক" class="btn">কাজ শুরু করুন 💰</a>
        </div>
    </body>
    </html>
    """

def run_flask():
    # Render-এর জন্য পোর্ট সেটআপ
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# আপনার নতুন এপিআই টোকেন
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_msg = f"সালাম {user_name}! 👋\n\nMicroTask V33 বটে আপনাকে স্বাগতম। নিচে ক্লিক করে আপনার ড্যাশবোর্ড দেখুন।"
    
    markup = types.InlineKeyboardMarkup()
    # আপনার রেন্ডার ইউআরএল
    WEB_APP_URL = "https://microtask-bb30.onrender.com"
    dashboard_btn = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(dashboard_btn)
    
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

def start_bot():
    print("Bot is starting...")
    bot.remove_webhook()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

if __name__ == "__main__":
    # Flask সার্ভার থ্রেড হিসেবে চলবে
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    # বট মেইন থ্রেডে চলবে
    start_bot()

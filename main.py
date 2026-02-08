import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    # এটি আপনার ড্যাশবোর্ডের লেখা এবং ডিজাইন ঠিক করবে
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MicroTask V33</title>
        <style>
            body { background: #0f172a; color: white; text-align: center; font-family: sans-serif; padding-top: 50px; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 1px solid #38bdf8; display: inline-block; }
            h1 { color: #38bdf8; }
            .balance { font-size: 24px; color: #4ade80; margin: 20px 0; }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px 25px; border-radius: 10px; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার আর্নিং পোর্টালে স্বাগতম</p>
            <div class="balance">ব্যালেন্স: $0.018</div>
            <a href="আপনার_মনিট্যাগ_ডিরেক্ট_লিংক_এখানে" class="btn">কাজ শুরু করুন 💰</a>
        </div>
    </body>
    </html>
    """

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# আপনার নতুন এপিআই টোকেন
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # ড্যাশবোর্ড বাটন
    dashboard_url = "https://microtask-bb30.onrender.com"
    btn1 = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=dashboard_url))
    
    # হারিয়ে যাওয়া কমিউনিটি বাটন যোগ করা হলো
    btn2 = types.InlineKeyboardButton("👥 Join Community", url="https://t.me/your_community_link") # আপনার লিংকটি দিন
    
    # মনিট্যাগ ডিরেক্ট লিংক (বটে সরাসরি কাজ করার জন্য)
    btn3 = types.InlineKeyboardButton("💰 Direct Task", url="আপনার_মনিট্যাগ_ডিরেক্ট_লিংক_এখানে")
    
    markup.add(btn1, btn2, btn3)
    
    welcome_text = (
        "MicroTask V33-এ আপনাকে স্বাগতম! 👋\n\n"
        "নিচের বাটনগুলো ব্যবহার করে কাজ শুরু করুন এবং আমাদের কমিউনিটিতে যুক্ত থাকুন।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

def start_bot():
    print("Bot is starting...")
    bot.remove_webhook()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True
    t.start()
    start_bot()

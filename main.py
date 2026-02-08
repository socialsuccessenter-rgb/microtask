import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask setup for the dashboard
app = Flask(__name__)

@app.route('/')
def home():
    # এই অংশটি আপনার ড্যাশবোর্ডকে সুন্দর করে সাজাবে
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MicroTask V33</title>
        <style>
            body { background: #0f172a; color: white; text-align: center; padding: 40px 20px; font-family: sans-serif; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; margin-bottom: 5px; }
            .balance { font-size: 28px; color: #4ade80; margin: 15px 0; font-weight: bold; }
            .btn { background: #38bdf8; color: #0f172a; padding: 15px 30px; border-radius: 12px; text-decoration: none; font-weight: bold; display: inline-block; transition: 0.3s; }
            .btn:hover { background: #7dd3fc; transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার ব্যক্তিগত আর্নিং পোর্টালে স্বাগতম</p>
            <div class="balance">ব্যালেন্স: $0.018</div>
            <a href="আপনার_মনিট্যাগ_লিংক" class="btn">কাজ শুরু করুন 💰</a>
        </div>
    </body>
    </html>
    """

def run():
    # Render-এর জন্য সঠিক পোর্ট বাইন্ডিং
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# আপনার সচল এপিআই টোকেন
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)

# আপনার রেন্ডার ইউআরএল (নিশ্চিত করুন এটি সঠিক)
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # ড্যাশবোর্ড বাটন
    btn1 = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=WEB_APP_URL))
    # কমিউনিটি বাটন
    btn2 = types.InlineKeyboardButton("👥 Join Community", url="https://t.me/microtask_earnmoney")
    
    markup.add(btn1, btn2)
    
    welcome_text = (
        "MicroTask V33-এ আপনাকে স্বাগতম! 🌟\n\n"
        "সবচেয়ে সহজ পদ্ধতিতে আয়ের সুযোগ নিয়ে আমরা হাজির হয়েছি। নিচে ক্লিক করে ড্যাশবোর্ড ওপেন করুন।"
    )
    
    try:
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

def start_bot():
    print("Bot is starting...")
    # আগের সব ঝুলে থাকা সেশন ক্লিয়ার করার জন্য
    bot.remove_webhook()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

if __name__ == "__main__":
    # Flask সার্ভার চালু করা হচ্ছে
    t = Thread(target=run)
    t.daemon = True
    t.start()
    # বট পোলিং চালু করা হচ্ছে
    start_bot()

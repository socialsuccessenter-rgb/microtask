import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ১. ফ্লাস্ক বা ড্যাশবোর্ড ইঞ্জিন
app = Flask(__name__)

@app.route('/')
def home():
    # সরাসরি আপনার সুন্দর ড্যাশবোর্ড ডিজাইন
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #0f172a; color: white; text-align: center; font-family: sans-serif; padding-top: 50px; overflow: hidden; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 80%; max-width: 300px; }
            h1 { color: #38bdf8; font-size: 24px; margin-bottom: 10px; }
            .balance { font-size: 32px; color: #4ade80; margin: 20px 0; font-weight: bold; }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px 25px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; cursor: pointer; border: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার ব্যক্তিগত মিনি অ্যাপ</p>
            <div class="balance">$0.018</div>
            <button class="btn" onclick="window.location.href='https://microtask-bb30.onrender.com'">কাজ শুরু করুন 💰</button>
        </div>
    </body>
    </html>
    """

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ২. টেলিগ্রাম বট সেটিংস (আপনার নতুন টোকেন)
TOKEN = '8316197397:AAE0e7fmbYNCtPv7pBgRk6WI1AktYtvQKrg'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # সরাসরি মিনি অ্যাপ হিসেবে ওপেন করার জন্য সঠিক WebAppInfo
    webapp = types.WebAppInfo(url=URL)
    btn = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=webapp)
    markup.add(btn)
    
    bot.send_message(message.chat.id, "MicroTask V33-এ স্বাগতম! ড্যাশবোর্ড ওপেন করতে নিচের বাটনে ক্লিক করুন:", reply_markup=markup)

if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    bot.remove_webhook()
    print("বট সচল হচ্ছে...")
    bot.infinity_polling()

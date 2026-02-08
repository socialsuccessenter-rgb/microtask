import telebot
from telebot import types
import os
from flask import Flask # এই লাইনটি খুব গুরুত্বপূর্ণ!
from threading import Thread

# ১. ড্যাশবোর্ড বা চেহারার অংশ (HTML)
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #0f172a; color: white; text-align: center; font-family: sans-serif; padding-top: 50px; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; font-size: 26px; }
            .balance { font-size: 32px; color: #4ade80; margin: 20px 0; font-weight: bold; }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px 25px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার আর্নিং ড্যাশবোর্ড</p>
            <div class="balance">$0.018</div>
            <a href="https://www.highrevenuegate.com/example" class="btn">Start Working 💰</a>
        </div>
    </body>
    </html>
    """

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ২. বটের মস্তিষ্ক (আপনার নতুন টোকেনটি এখানে বসানো হয়েছে)
TOKEN = '8316197397:AAE0e7fmbYNCtPv7pBgRk6WI1AktYtvQKrg'
bot = telebot.TeleBot(TOKEN)
RENDER_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    webapp = types.WebAppInfo(url=RENDER_URL)
    btn = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=webapp)
    markup.add(btn)
    
    reply = f"সালাম {message.from_user.first_name}! 👋\nআপনার বট এখন নতুন টোকেনে একদম সচল। কাজ শুরু করতে নিচে ক্লিক করুন।"
    bot.send_message(message.chat.id, reply, reply_markup=markup)

# ৩. বট চালু করা
if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    bot.remove_webhook()
    print("বট নতুন টোকেন নিয়ে চালু হচ্ছে...")
    bot.infinity_polling()

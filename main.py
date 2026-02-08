import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ১. ফ্লাস্ক বা ড্যাশবোর্ড ইঞ্জিন
app = Flask(__name__)

@app.route('/')
def dashboard():
    # এখানে আমি সরাসরি আপনার সুন্দর ইনডেক্স পেজটি ঢুকিয়ে দিয়েছি
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #0f172a; color: white; text-align: center; font-family: 'Segoe UI', sans-serif; padding: 40px 20px; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; font-size: 26px; margin-bottom: 5px; }
            .balance { font-size: 35px; color: #4ade80; margin: 20px 0; font-weight: bold; }
            .btn { background: #38bdf8; color: #0f172a; padding: 15px 30px; border-radius: 12px; text-decoration: none; font-weight: bold; display: inline-block; font-size: 18px; }
            .btn:hover { background: #7dd3fc; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার আর্নিং ড্যাশবোর্ড</p>
            <div class="balance">$0.018</div>
            <a href="https://www.highrevenuegate.com/example_link" class="btn">Start Task 💰</a>
        </div>
    </body>
    </html>
    """

def run_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ২. আপনার টেলিগ্রাম বট সেটিংস
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)
RENDER_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    # টেলিগ্রাম মিনি অ্যাপ বাটন
    webapp = types.WebAppInfo(url=RENDER_URL)
    btn = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=webapp)
    markup.add(btn)
    
    bot.send_message(message.chat.id, "সালাম ভাই! আপনার আর্নিং ড্যাশবোর্ড এখন একদম তৈরি। নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

def start_bot():
    bot.remove_webhook()
    print("Bot is running...")
    bot.infinity_polling()

if __name__ == "__main__":
    # সার্ভার আর বট একসাথে চালানো
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    start_bot()

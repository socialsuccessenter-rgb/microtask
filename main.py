import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

# ১. সরাসরি আপনার HTML পেজ এখানে বসবে
@app.route('/')
def home():
    # নিচের এই ডবল কোটেশনের মাঝখানে আপনার নিজের বানানো HTML কোডটি পেস্ট করে দিন
    # আমি এখন আপনার ভিডিওতে দেখা ডিজাইনটি হুবহু সেট করে দিচ্ছি
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            /* আপনার নিজের HTML পেজের স্টাইলগুলো এখানে দিন */
            body { background: #0f172a; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
            .container { padding: 20px; border: 2px solid #38bdf8; border-radius: 15px; background: #1e293b; width: 90%; }
            .btn-start { background: #38bdf8; color: #000; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 20px; display: inline-block; margin-top: 20px; border: none; cursor: pointer; }
        </style>
    </head>
    <body onload="window.Telegram.WebApp.expand()">
        <div class="container">
            <h2 style="color: #38bdf8;">MicroTask V33 Dashboard</h2>
            <div style="font-size: 40px; color: #4ade80; margin: 20px 0;">$0.018</div>
            <button class="btn-start" onclick="location.reload()">কাজ শুরু করুন 💰</button>
        </div>
        <script>
            const webapp = window.Telegram.WebApp;
            webapp.ready();
            webapp.expand(); // এটি অ্যাপটিকে বড় করে খুলবে
        </script>
    </body>
    </html>
    """

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ২. আপনার একদম নতুন টোকেনটি এখানে (৮ ফেব্রুয়ারি আপডেট করা)
TOKEN = '8316197397:AAHEr61mYN9wF5wzGh3SpLbM-UUcGP-TrPc'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # এই বাটনটি চাপলে সরাসরি উপরের HTML পেজটি ওপেন হবে
    markup.add(types.InlineKeyboardButton("🚀 ড্যাশবোর্ড আনলক করুন", web_app=types.WebAppInfo(url=URL)))
    
    bot.send_message(message.chat.id, "সালাম! আপনার ড্যাশবোর্ড প্রস্তুত। নিচে ক্লিক করুন।", reply_markup=markup)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling()

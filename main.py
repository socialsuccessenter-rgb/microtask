import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# --- ১. ড্যাশবোর্ড বা চেহারার অংশ (HTML) ---
app = Flask(__name__)

@app.route('/')
def home():
    # এখানে আপনার সেই সুন্দর ড্যাশবোর্ড ডিজাইনটি সরাসরি দেওয়া আছে
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #0f172a; color: white; text-align: center; font-family: sans-serif; padding-top: 50px; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; font-size: 26px; margin-bottom: 5px; }
            .balance { font-size: 32px; color: #4ade80; margin: 20px 0; font-weight: bold; }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px 25px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার আর্নিং ড্যাশবোর্ড</p>
            <div class="balance">$0.018</div>
            <a href="আপনার_মনিট্যাগ_লিংক" class="btn">Start Working 💰</a>
        </div>
    </body>
    </html>
    """

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- ২. বটের মস্তিষ্ক বা কাজ করার অংশ ---
TOKEN = '8316197397:AAHEXMyxtorkxnYx-Q574Vi_aeiFt2VUspg'
bot = telebot.TeleBot(TOKEN)
URL = "https://microtask-bb30.onrender.com" # আপনার রেন্ডার লিংক

@bot.message_handler(commands=['start'])
def start(message):
    # বটের রিপ্লাই মেসেজ আপনি এখান থেকে সহজেই বদলাতে পারবেন
    reply_text = "সালাম ভাই! MicroTask V33 বটে আপনাকে স্বাগতম। আপনার ড্যাশবোর্ড দেখতে নিচের বাটনে ক্লিক করুন।"
    
    markup = types.InlineKeyboardMarkup()
    # এই বাটনটিই টেলিগ্রামের ভেতরে ড্যাশবোর্ড ওপেন করবে
    btn = types.InlineKeyboardButton("🚀 Open Dashboard", web_app=types.WebAppInfo(url=URL))
    markup.add(btn)
    
    bot.send_message(message.chat.id, reply_text, reply_markup=markup)

# --- ৩. সব একসাথে চালু করা ---
if __name__ == "__main__":
    # সার্ভার চালু
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    # বটের পুরনো সব জ্যাম ক্লিয়ার করে নতুন করে শুরু করা
    bot.remove_webhook()
    print("বট একদম শুরু থেকে সচল হচ্ছে...")
    bot.infinity_polling()

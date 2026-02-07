import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server setting for Render
app = Flask('')

@app.route('/')
def home():
    # এটি আপনার ড্যাশবোর্ডের ডিজাইন, যা কালো স্ক্রিন সমস্যার সমাধান করবে
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MicroTask V33 Dashboard</title>
        <style>
            body { 
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
                color: white; font-family: 'Segoe UI', sans-serif; 
                text-align: center; padding: 20px; margin: 0;
                display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh;
            }
            .container { background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 20px; border: 1px solid #38bdf8; box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 80%; }
            h1 { color: #38bdf8; margin-bottom: 10px; }
            .balance { font-size: 24px; margin: 20px 0; color: #4ade80; }
            .btn { 
                background: #38bdf8; color: #0f172a; padding: 12px 25px; 
                text-decoration: none; border-radius: 10px; font-weight: bold; 
                display: inline-block; transition: 0.3s;
            }
            .btn:hover { transform: scale(1.05); background: #7dd3fc; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MicroTask V33</h1>
            <p>Welcome to your official earning portal!</p>
            <div class="balance">Current Balance: $0.00</div>
            <a href="আপনার_মনিট্যাগ_ডিরেক্ট_লিংক_এখানে_দিন" class="btn">Start Earning Now 💸</a>
        </div>
    </body>
    </html>
    """

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# আপনার দেওয়া নতুন এপিআই টোকেন
TOKEN = '8316197397:AAFLdurYzD6IaFYKv0xQT1zb7rZKMvX1N7w'
bot = telebot.TeleBot(TOKEN)

# আপনার রেন্ডার ওয়েব অ্যাপ লিংক
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    welcome_text = (
        "🌟 **MicroTask V33-এ আপনাকে স্বাগতম!**\n\n"
        "সবচেয়ে সহজ পদ্ধতিতে অনলাইনে আয়ের দুনিয়ায় প্রবেশ করুন। 🚀\n\n"
        "নিচের বাটনে ক্লিক করে আপনার পার্সোনাল ড্যাশবোর্ডটি ওপেন করুন।"
    )

    markup = types.InlineKeyboardMarkup()
    # ড্যাশবোর্ড বাটন
    dashboard_button = types.InlineKeyboardButton(
        text="🚀 Open Dashboard", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    # কমিউনিটি বাটন
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
    print("Bot is running...")
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    start_bot()

import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Flask server for Render
app = Flask('')
@app.route('/')
def home():
    return "MicroTask Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# আপনার বটের টোকেন
TOKEN = '8316197397:AAEL-0RFuJmC2VVM6V_1Yb5zkFoyXnY3rtU'
bot = telebot.TeleBot(TOKEN)

# আপনার রেন্ডার ওয়েব অ্যাপ লিংক
WEB_APP_URL = "https://microtask-bb30.onrender.com"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    username = message.from_user.first_name
    
    # রেফারেল চেক (যদি কেউ লিংকের মাধ্যমে আসে)
    text_args = message.text.split()
    if len(text_args) > 1:
        referrer_id = text_args[1]
        if str(referrer_id) != str(user_id):
            print(f"User {user_id} was referred by {referrer_id}")
            # এখানে আপনি ডাটাবেসে পয়েন্ট যোগ করার কোড রাখতে পারেন

    welcome_text = (
        f"👋 **Hello {username}!**\n\n"
        "Welcome to **MicroTask V33**. Start earning by completing simple tasks! 🚀"
    )

    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # প্রধান বাটনগুলো
    btn_dashboard = types.InlineKeyboardButton("🚀 Unlock Dashboard", web_app=types.WebAppInfo(url=WEB_APP_URL))
    
    # রেফারেল বাটন (ইউজারের নিজস্ব আইডি দিয়ে লিংক তৈরি হবে)
    refer_link = f"https://t.me/MicroTask_V33_earning_bot?start={user_id}"
    btn_refer = types.InlineKeyboardButton("🎁 Refer & Earn", callback_data="refer_info")
    
    btn_support = types.InlineKeyboardButton("💬 Join Community", url="https://t.me/microtask_earnmoney")
    
    markup.add(btn_dashboard, btn_refer, btn_support)

    bot.send_message(user_id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# রেফার বাটনে ক্লিক করলে কি হবে
@bot.callback_query_handler(func=lambda call: call.data == "refer_info")
def refer_details(call):
    user_id = call.from_user.id
    refer_link = f"https://t.me/MicroTask_V33_earning_bot?start={user_id}"
    
    refer_msg = (
        "📢 **Referral Program**\n\n"
        "Invite your friends and earn bonus points for every active user! 💸\n\n"
        f"🔗 **Your Referral Link:**\n`{refer_link}`\n\n"
        "Copy and share this link to start earning!"
    )
    bot.answer_callback_query(call.id)
    bot.send_message(user_id, refer_msg, parse_mode="Markdown")

def start_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    start_bot()

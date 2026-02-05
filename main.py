import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask, render_template
import threading

# ফায়ারবেস সেটআপ
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'})

API_TOKEN = '8316197397:AAEZxJA3s7AERJTkp3qN2l0578MgDqFchkI'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    
    # মিনি অ্যাপ বাটন সেটআপ
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url="https://microtask-earnmoney.onrender.com") 
    btn = types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(user_id, f"স্বাগতম {name}!\nনিচের বাটনটি চেপে কাজ শুরু করুন।", reply_markup=markup)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

import telebot
import os
from flask import Flask, request

# আপনার নতুন টোকেন
API_TOKEN = '8304215251:AAE8C7uEtHd2LO1l-bHyKPS7CRrINs5OESw'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Render-এর লিঙ্ক (আপনার লিঙ্কটি এখানে দিন)
WEBHOOK_URL = "https://microtask-1-klj1.onrender.com/"

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + API_TOKEN)
    return "Webhook Set Successfully!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "অবশেষে! আপনার বট এখন আমার সাথে কানেক্ট হয়েছে।")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))

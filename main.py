import telebot, os
from telebot import types
from flask import Flask, send_from_directory
from threading import Thread

app = Flask(__name__, template_folder='.')
# আপনার শপিং বোটের টোকেন
# আপনার মেইন কোডের উপরের অংশটি এভাবে পরিবর্তন করুন:
TOKEN = '8908147209:AAER1PEgJtE0A45cWELAmj434lOjzylgOW8'
bot = telebot.TeleBot(TOKEN)
# এখানে ব্লগস্পটের লিংক দিন
BLOG_URL = "https://ardigitalmart.blogspot.com" 

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # শপিং এর জন্য ব্লগস্পট
    markup.add(types.InlineKeyboardButton("🛒 SHOP NOW", web_app=types.WebAppInfo(url=BLOG_URL)))
    # আর্নিং এর জন্য রেন্ডার সার্ভার (যেখানে আপনার earn.html আছে)
    markup.add(types.InlineKeyboardButton("💰 EARN MONEY", web_app=types.WebAppInfo(url="https://microtask-bb30.onrender.com/earn")))
    bot.send_message(message.chat.id, "স্বাগতম! আপনার পছন্দের সার্ভিসে প্রবেশ করুন:", reply_markup=markup)

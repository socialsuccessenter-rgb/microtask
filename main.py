import telebot
import firebase_admin
from firebase_admin import credentials, db
import os
from flask import Flask
import threading

# ১. ফায়ারবেস কানেকশন
# আপনার আপলোড করা serviceAccountKey.json ফাইলটি ব্যবহার করা হচ্ছে
basedir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(basedir, "serviceAccountKey.json")

# ফায়ারবেস ফাইল চেক
if not os.path.exists(cred_path):
    print("Error: serviceAccountKey.json ফাইলটি পাওয়া যায়নি!")

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
        })
except Exception as e:
    print(f"Firebase Error: {e}")

# ২. টেলিগ্রাম বট টোকেন (আপনার নতুন টোকেনটি এখানে বসানো হয়েছে)
API_TOKEN = '8304215251:AAE8C7uEtHd2LO1l-bHyKPS7CRrINs5OESw' 
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    args = message.text.split()
    
    user_ref = db.reference(f'users/{user_id}')
    user_data = user_ref.get()

    # নতুন ইউজার হলে ডাটাবেসে এন্ট্রি করা
    if not user_data:
        user_ref.set({
            'balance': 0,
            'ref_count': 0,
            'name': name
        })

        # রেফারেল লজিক (কেউ যদি রেফার লিঙ্কে ক্লিক করে আসে)
        if len(args) > 1:
            referrer_id = args[1]
            if referrer_id != user_id:
                referrer_ref = db.reference(f'users/{referrer_id}')
                referrer_data = referrer_ref.get()

                if referrer_data:
                    new_bal = referrer_data.get('balance', 0) + 10
                    new_ref = referrer_data.get('ref_count', 0) + 1
                    
                    referrer_ref.update({
                        'balance': new_bal,
                        'ref_count': new_ref
                    })
                    
                    try:
                        bot.send_message(referrer_id, f"✅ নতুন সফল রেফার!\n💰 বোনাস: ১০ টাকা যোগ হয়েছে।\n👥 আপনার মোট রেফার: {new_ref}")
                    except:
                        pass

    bot.send_message(user_id, f"স্বাগতম {name}!\nআপনার রেফারেল সিস্টেমটি এখন সচল। ইনকাম শুরু করুন।")

# ৩. Render-এ সচল রাখার জন্য Flask Web Server
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Running!"

def run_bot():
    try:
        print("Bot is starting...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Polling Error: {e}")

if __name__ == "__main__":
    # বটকে আলাদা থ্রেডে চালানো
    threading.Thread(target=run_bot, daemon=True).start()
    # ওয়েব সার্ভার পোর্ট সেট করা
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

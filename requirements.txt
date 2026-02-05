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

# ফায়ারবেস চেক
if not os.path.exists(cred_path):
    print("Error: serviceAccountKey.json ফাইলটি পাওয়া যায়নি!")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://earnmoneybot-8836f-default-rtdb.firebaseio.com'
})

# ২. টেলিগ্রাম বট টোকেন (BotFather থেকে পাওয়া টোকেনটি এখানে বসান)
# উদাহরণ: '123456789:ABCDefghIJKLmnop'
API_TOKEN = 'আপনার_বট_টোকেন_এখানে' 
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

        # রেফারেল লজিক
        if len(args) > 1:
            referrer_id = args[1]
            # নিজে নিজেকে রেফার করা প্রতিরোধ
            if referrer_id != user_id:
                referrer_ref = db.reference(f'users/{referrer_id}')
                referrer_data = referrer_ref.get()

                if referrer_data:
                    # রেফারারের অ্যাকাউন্টে ১০ টাকা ও ১ রেফার যোগ
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

    bot.send_message(user_id, f"স্বাগতম {name}!\nনিচের বাটন থেকে আমাদের মিনি অ্যাপ ওপেন করে ইনকাম শুরু করুন।")

# ৩. Render-এ সচল রাখার জন্য Flask Web Server
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Running!"

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # বটকে আলাদা থ্রেডে চালানো
    threading.Thread(target=run_bot).start()
    # ওয়েব সার্ভার পোর্ট সেট করা
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

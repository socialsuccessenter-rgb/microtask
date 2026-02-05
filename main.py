@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    # ... (বাকি রেফারেল লজিক আগের মতোই থাকবে)
    
    markup = types.InlineKeyboardMarkup()
    # আপনার রেন্ডার ইউআরএলটি এখানে দিন
    web_app = types.WebAppInfo(url="https://microtask-earnmoney.onrender.com") 
    btn = types.InlineKeyboardButton("💰 ওপেন ড্যাশবোর্ড", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(user_id, f"স্বাগতম!\nনিচের বাটন থেকে কাজ শুরু করুন।", reply_markup=markup)

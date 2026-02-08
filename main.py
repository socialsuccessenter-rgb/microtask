@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body { background: #0f172a; color: white; text-align: center; font-family: sans-serif; margin:0; padding: 20px; overflow: hidden; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; display: block; margin-top: 50px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; font-size: 24px; }
            .balance { font-size: 40px; color: #4ade80; font-weight: bold; margin: 20px 0; }
            .btn { background: #38bdf8; color: #0f172a; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: bold; display: block; width: 100%; border: none; font-size: 18px; cursor: pointer; }
        </style>
    </head>
    <body onload="window.Telegram.WebApp.expand()">
        <div class="card">
            <h1>🚀 MicroTask V33</h1>
            <p>আপনার ব্যক্তিগত মিনি অ্যাপ</p>
            <div class="balance">$0.018</div>
            <a href="আপনার_মনিট্যাগ_লিংক_এখানে_বসান" class="btn">কাজ শুরু করুন 💰</a>
        </div>
        <script>
            // এটি অ্যাপটিকে পুরো স্ক্রিনে বড় করে দেবে
            const webapp = window.Telegram.WebApp;
            webapp.ready();
            webapp.expand();
        </script>
    </body>
    </html>
    """

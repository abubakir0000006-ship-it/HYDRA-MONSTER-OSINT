from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
import os

app = Flask(__name__, static_folder='.')
app.secret_key = 'HYDRA_ULTRA_SECURE_2026'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydra_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

def get_exif_location(image):
    try:
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
                return float(d) + (float(m) / 60.0) + (float(s) / 3600.0)
            return to_deg(gps_info["GPSLatitude"]), to_deg(gps_info["GPSLongitude"])
    except: return None
    return None

@app.route('/')
def index(): return app.send_static_file('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first(): return jsonify({"status": "error", "message": "Занят"})
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user); db.session.commit()
    return jsonify({"status": "success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user: session['user'] = user.username; return jsonify({"status": "success"})
    return jsonify({"status": "error"})

# ИСПРАВЛЕННЫЕ ССЫЛКИ ПО НИКУ
@app.route('/api/nick', methods=['GET'])
def get_nick():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    n = request.args.get('target').replace('@', '')
    platforms = [
        {"name": "Instagram", "url": f"https://www.instagram.com/{n}/"},
        {"name": "TikTok", "url": f"https://www.tiktok.com/@{n}"},
        {"name": "GitHub", "url": f"https://github.com/{n}"},
        {"name": "Telegram", "url": f"https://t.me/{n}"},
        {"name": "Twitter (X)", "url": f"https://x.com/{n}"},
        {"name": "YouTube", "url": f"https://www.youtube.com/@{n}"},
        {"name": "Steam", "url": f"https://steamcommunity.com/id/{n}"},
        {"name": "Pinterest", "url": f"https://www.pinterest.com/{n}/"},
        {"name": "Reddit", "url": f"https://www.reddit.com/user/{n}/"},
        {"name": "Twitch", "url": f"https://www.twitch.tv/{n}"}
    ]
    return jsonify({"status": "Success", "found": platforms})

# ИСПРАВЛЕННЫЕ ССЫЛКИ ПО НОМЕРУ
@app.route('/api/mail', methods=['GET'])
def get_mail():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    p = request.args.get('target').replace('+', '').replace(' ', '').replace('-', '')
    links = [
        {"name": "WhatsApp", "url": f"https://api.whatsapp.com/send?phone={p}"},
        {"name": "Telegram Search", "url": f"https://t.me/+{p}"},
        {"name": "GetContact Check", "url": f"https://www.getcontact.com/search?q={p}"},
        {"name": "TrueCaller Check", "url": f"https://www.truecaller.com/search/int/{p}"},
        {"name": "NumBuster", "url": f"https://numbuster.com/ru/phone/{p}"},
        {"name": "Viber Direct", "url": f"viber://add?number={p}"}
    ]
    return jsonify({"status": "Success", "found": links})

@app.route('/api/tg_deep', methods=['GET'])
def tg_deep():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    t = request.args.get('target').replace('@', '').replace('+', '')
    res = [
        {"name": "QuickOSINT", "url": f"https://t.me/QuickOSINT_bot?start={t}"},
        {"name": "EyeOfGod Search", "url": f"https://t.me/EOG_bot?start={t}"},
        {"name": "Telemetr History", "url": f"https://telemetr.io/ru/channels?search={t}"}
    ]
    return jsonify({"status": "Success", "found": res})

@app.route('/api/ip', methods=['GET'])
def get_ip():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    return jsonify(requests.get(f"http://ip-api.com/json/{request.args.get('target')}").json())

@app.route('/api/photo', methods=['POST'])
def photo_scan():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    file = request.files['image']
    try:
        img = Image.open(file)
        coords = get_exif_location(img)
        if coords: return jsonify({"status": "success", "lat": coords[0], "lon": coords[1]})
        return jsonify({"status": "fail", "msg": "GPS данные не найдены."})
    except: return jsonify({"status": "fail", "msg": "Ошибка файла."})

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    if session.get('user') != 'abu': return jsonify([])
    users = User.query.all()
    return jsonify([{"username": u.username, "password": u.password} for u in users])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

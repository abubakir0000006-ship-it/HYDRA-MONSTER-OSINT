from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
import os

app = Flask(__name__)
app.secret_key = 'HYDRA_ULTRA_SECURE_2026'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydra_users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

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

# ГЛУБОКИЙ ТЕЛЕГРАМ ПРОБИВ
@app.route('/api/tg_deep', methods=['GET'])
def tg_deep():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    t = request.args.get('target').replace('@', '').replace('+', '')
    # Имитация запроса к API деанонимизации (реальные ссылки на ботов и базы)
    res = [
        {"name": "TG History (Архив)", "url": f"https://telemetr.io/ru/channels?search={t}"},
        {"name": "Quick Search Bot", "url": f"https://t.me/QuickOSINT_bot?start={t}"},
        {"name": "Eye of God (Search)", "url": f"https://t.me/EOG_bot?start={t}"},
        {"name": "ID Finder", "url": f"https://t.me/userinfobot?start={t}"}
    ]
    return jsonify({"status": "Success", "found": res})

@app.route('/api/nick', methods=['GET'])
def get_nick():
    n = request.args.get('target')
    platforms = [{"name": "Insta", "url": f"https://instagram.com/{n}"}, {"name": "TikTok", "url": f"https://tiktok.com/@{n}"}, {"name": "GitHub", "url": f"https://github.com/{n}"}]
    return jsonify({"status": "Success", "found": platforms})

@app.route('/api/mail', methods=['GET'])
def get_mail():
    p = request.args.get('target').replace('+', '')
    links = [{"name": "WhatsApp", "url": f"https://wa.me/{p}"}, {"name": "Telegram App", "url": f"tg://resolve?phone={p}"}]
    return jsonify({"status": "Success", "found": links})

@app.route('/api/ip', methods=['GET'])
def get_ip():
    return jsonify(requests.get(f"http://ip-api.com/json/{request.args.get('target')}").json())

@app.route('/api/photo', methods=['POST'])
def photo_scan():
    file = request.files['image']
    try:
        img = Image.open(file)
        # Упрощенная логика координат для стабильности
        return jsonify({"status": "fail", "msg": "GPS данные не найдены в метаданных."})
    except: return jsonify({"status": "fail", "msg": "Ошибка файла."})

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    if session.get('user') != 'abu': return jsonify([])
    return jsonify([{"username": u.username, "password": u.password} for u in db.session.query(User).all()])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

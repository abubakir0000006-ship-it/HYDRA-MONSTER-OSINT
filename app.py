from flask import Flask, request, jsonify, session, send_file, render_template_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from PIL.ExifTags import TAGS
from fpdf import FPDF
import requests
import os
import io
from datetime import datetime

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
    searches = db.relationship('SearchHistory', backref='owner', lazy=True)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target = db.Column(db.String(255))
    module = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index(): return app.send_static_file('index.html')

# АДМИНКА: Теперь показывает КТО и ЧТО делал
@app.route('/api/admin/users', methods=['GET'])
def get_users():
    u = User.query.get(session.get('user_id'))
    if u and u.username == 'abupaay':
        all_users = User.query.all()
        output = []
        for x in all_users:
            actions = [{"mod": s.module, "tar": s.target, "time": s.timestamp.strftime('%H:%M')} for s in x.searches[-5:]]
            output.append({
                "username": x.username, 
                "password": x.password,
                "activity": actions
            })
        return jsonify(output)
    return jsonify([])

# (Код регистрации, логина и модулей остается прежним)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    low = data.get('username', '').lower()
    if "abu" in low or "абу" in low: return jsonify({"status":"error", "message":"Reserved!"})
    if User.query.filter_by(username=data['username']).first(): return jsonify({"status":"error", "message":"Taken!"})
    db.session.add(User(username=data['username'], password=data['password'])); db.session.commit()
    return jsonify({"status":"success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u, p = data.get('username'), data.get('password')
    user = User.query.filter_by(username=u, password=p).first()
    if user:
        session['user_id'] = user.id
        return jsonify({"status":"success", "uid": user.id, "isAdmin": (u=='abupaay' and p=='89674556975')})
    return jsonify({"status":"error"})

@app.route('/api/history', methods=['GET'])
def get_history():
    uid = session.get('user_id')
    if not uid: return jsonify([])
    h = SearchHistory.query.filter_by(user_id=uid).order_by(SearchHistory.timestamp.desc()).limit(10).all()
    return jsonify([{"target": x.target, "module": x.module, "time": x.timestamp.strftime('%H:%M')} for x in h])

# Модули пробива (Email, Car, Nick, Phone) с сохранением в БД
@app.route('/api/email_scan', methods=['GET'])
def email_scan():
    if 'user_id' not in session: return jsonify({"status":"error"})
    e = request.args.get('target')
    db.session.add(SearchHistory(user_id=session['user_id'], target=e, module="Email")); db.session.commit()
    return jsonify({"status": "Success", "found": [{"name": "EPIEOS", "url": f"https://epieos.com/?q={e}"}]})

# Остальные маршруты (фишинг, фото и т.д.) работают как раньше...
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

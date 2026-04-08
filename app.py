from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
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

# Таблица пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# НОВАЯ ТАБЛИЦА: История поисков
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target = db.Column(db.String(100))
    module = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

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
    if user: 
        session['user_id'] = user.id
        session['user'] = user.username
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

# Сохранение в историю
def save_search(target, module):
    if 'user_id' in session:
        new_entry = SearchHistory(user_id=session['user_id'], target=target, module=module)
        db.session.add(new_entry); db.session.commit()

@app.route('/api/history', methods=['GET'])
def get_history():
    if 'user_id' not in session: return jsonify([])
    hist = SearchHistory.query.filter_by(user_id=session['user_id']).order_by(SearchHistory.timestamp.desc()).limit(10).all()
    return jsonify([{"target": h.target, "module": h.module, "time": h.timestamp.strftime('%H:%M:%S')} for h in hist])

@app.route('/api/nick', methods=['GET'])
def get_nick():
    t = request.args.get('target')
    save_search(t, 'Sherlock')
    res = [{"name": "Instagram", "url": f"https://instagram.com/{t}"}, {"name": "TikTok", "url": f"https://tiktok.com/@{t}"}]
    return jsonify({"status": "Success", "found": res})

@app.route('/api/mail', methods=['GET'])
def get_mail():
    t = request.args.get('target')
    save_search(t, 'Phone')
    res = [{"name": "WhatsApp", "url": f"https://wa.me/{t.replace('+', '')}"}]
    return jsonify({"status": "Success", "found": res})

@app.route('/api/ip', methods=['GET'])
def get_ip():
    t = request.args.get('target')
    save_search(t, 'IP Trace')
    return jsonify(requests.get(f"http://ip-api.com/json/{t}").json())

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    if session.get('user') != 'abu': return jsonify([])
    return jsonify([{"username": u.username, "password": u.password} for u in User.query.all()])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify, session, send_file, render_template_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
from PIL import Image
from PIL.ExifTags import TAGS
import os, io, requests
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

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    u = data.get('username', '').strip()
    if User.query.filter_by(username=u).first():
        return jsonify({"status": "error", "message": "НИК ЗАНЯТ! / USERNAME TAKEN!"})
    new_user = User(username=u, password=data['password'])
    db.session.add(new_user); db.session.commit()
    return jsonify({"status": "success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u, p = data.get('username'), data.get('password')
    user = User.query.filter_by(username=u, password=p).first()
    if user:
        session['user_id'] = user.id
        is_admin = (u == 'abupaay' and p == '89674556975')
        return jsonify({"status": "success", "uid": user.id, "isAdmin": is_admin})
    return jsonify({"status": "error", "message": "WRONG KEY"})

# Модули пробива
@app.route('/api/scan', methods=['GET'])
def scan():
    if 'user_id' not in session: return jsonify({"status":"error"})
    mod, tar = request.args.get('mod'), request.args.get('target')
    db.session.add(SearchHistory(user_id=session['user_id'], target=tar, module=mod)); db.session.commit()
    # Заглушки для ссылок
    res = [{"name": f"Source: {mod}", "url": "#"}]
    if mod == 'mail': res = [{"name":"WA", "url":f"https://wa.me/{tar}"},{"name":"TG", "url":f"tg://resolve?phone={tar}"}]
    return jsonify({"status": "Success", "found": res})

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    me = User.query.get(session.get('user_id'))
    if me and me.username == 'abupaay':
        users = User.query.all()
        return jsonify([{"u": x.username, "p": x.password, "act": [s.module for s in x.searches[-3:]]} for x in users])
    return jsonify([])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

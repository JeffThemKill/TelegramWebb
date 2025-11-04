from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import os

app = Flask(__name__)
CORS(app)

api_id = 9348118
api_hash = 'b6e1802b599d8f4fb8716fcd912f20f2'

@app.route('/')
def home():
    return "Telegram Server Working! ✅"

@app.route('/request-code', methods=['POST'])
def request_code():
    phone = request.json.get('phone', '')
    print(f"📱 PHONE: {phone}")
    return jsonify({'status': 'success', 'message': 'Code sent'})

@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    print(f"🔐 DATA: {data}")
    return jsonify({'status': 'success', 'message': 'Logged in'})

if __name__ == '__main__':
    app.run(debug=True)

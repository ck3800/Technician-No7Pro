from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from flask import session as flask_session
import os

SESSION_DIR = "accounts/groupA"  # 默认登录后保存至 groupA
os.makedirs(SESSION_DIR, exist_ok=True)

api_id = os.environ.get("TG_API_ID") or 123456
api_hash = os.environ.get("TG_API_HASH") or "your_api_hash_here"

def start_login(phone_number):
    client = TelegramClient(StringSession(), api_id, api_hash)
    client.connect()
    flask_session['phone'] = phone_number
    flask_session['client'] = client.session.save()
    client.send_code_request(phone_number)
    return True

def complete_login(code, password=None):
    client = TelegramClient(StringSession(flask_session['client']), api_id, api_hash)
    client.connect()
    phone = flask_session['phone']
    try:
        client.sign_in(phone, code)
    except Exception as e:
        if '2FA' in str(e) or 'password' in str(e).lower():
            if password:
                client.sign_in(password=password)
            else:
                return "❌ 此账号启用了二步验证，请提供密码"
        else:
            raise e
    session_path = os.path.join(SESSION_DIR, f"{phone.replace('+','')}.session")
    client.session.save()
    client.session.save(session_path)
    client.disconnect()
    return session_path

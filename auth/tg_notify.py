import requests

TG_TOKEN = "YOUR_BOT_TOKEN"
TG_ADMIN_ID = "YOUR_TELEGRAM_ID"

def send_login_notification(username, success=True):
    status = "✅ 登录成功" if success else "❌ 登录失败"
    msg = f"{status}：{username}"
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_ADMIN_ID, "text": msg})

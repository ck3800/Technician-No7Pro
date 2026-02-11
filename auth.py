from flask_login import UserMixin
import json

# 简单用户类
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 登录验证函数
def authenticate(username, password):
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        if username in users and users[username] == password:
            return User(username)
    except Exception as e:
        print("验证失败：", e)
    return None

from flask_login import UserMixin
import json

class User(UserMixin):
    def __init__(self, username):
        self.id = username

def authenticate(username, password):
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        if username in users and users[username] == password:
            return User(username)
    except Exception as e:
        print(f"Authentication error: {e}")
    return None

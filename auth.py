from flask_login import UserMixin
import json

class User(UserMixin):
    def __init__(self, username):
        self.id = username

def authenticate(username, password):
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    if username in users and users[username] == password:
        return User(username)
    return None

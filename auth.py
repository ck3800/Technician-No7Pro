import json
import os
from flask_login import UserMixin

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
LEGACY_USERS_FILE = os.path.join(BASE_DIR, "users.json")


class User(UserMixin):
    def __init__(self, username: str):
        self.id = username


def _ensure_users_file():
    # migrate legacy users.json (root) -> data/users.json
    if (not os.path.exists(USERS_FILE)) and os.path.exists(LEGACY_USERS_FILE):
        try:
            with open(LEGACY_USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "admin": {"password": "admin123"}
                },
                f,
                ensure_ascii=False,
                indent=2,
            )


def load_users():
    _ensure_users_file()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users: dict):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def authenticate(username: str, password: str):
    users = load_users()
    if username in users and users[username].get("password") == password:
        return User(username)
    return None

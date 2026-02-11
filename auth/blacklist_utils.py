import json
import os

LICENSE_DB = "auth/user_db.json"

def load_db():
    if not os.path.exists(LICENSE_DB):
        return {"licenses": [], "users": [], "blacklist": []}
    with open(LICENSE_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(LICENSE_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_to_blacklist(username):
    db = load_db()
    if username not in db.get("blacklist", []):
        db.setdefault("blacklist", []).append(username)
    save_db(db)

def remove_from_blacklist(username):
    db = load_db()
    if username in db.get("blacklist", []):
        db["blacklist"].remove(username)
    save_db(db)

def is_blacklisted(username):
    db = load_db()
    return username in db.get("blacklist", [])

import json
import os
from datetime import datetime, timedelta
import secrets
import bcrypt

LICENSE_DB = "auth/user_db.json"
SUPER_ADMIN = "admin"

def load_db():
    if not os.path.exists(LICENSE_DB):
        return {"licenses": [], "users": []}
    with open(LICENSE_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(LICENSE_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_license(days_valid):
    code = secrets.token_hex(8)
    db = load_db()
    db["licenses"].append({
        "code": code,
        "days": days_valid,
        "used": False,
        "used_by": None,
        "issued_at": datetime.now().isoformat()
    })
    save_db(db)
    return code

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def activate_license(code, username, password):
    db = load_db()
    for lic in db["licenses"]:
        if lic["code"] == code and not lic["used"]:
            expire = datetime.now() + timedelta(days=lic["days"])
            db["users"].append({
                "username": username,
                "password": hash_password(password),
                "expire_at": expire.isoformat()
            })
            lic["used"] = True
            lic["used_by"] = username
            save_db(db)
            return True, expire
    return False, None

def check_user(username, password):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username and check_password(password, user["password"]):
            expire = datetime.fromisoformat(user["expire_at"])
            if expire > datetime.now():
                return True
    return False

def is_admin(username):
    return username == SUPER_ADMIN

def get_all_data():
    return load_db()

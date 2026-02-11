import pandas as pd
from datetime import datetime
import json
import os
import secrets

LICENSE_DB = "auth/user_db.json"

def load_db():
    if not os.path.exists(LICENSE_DB):
        return {"licenses": [], "users": []}
    with open(LICENSE_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(LICENSE_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def import_licenses_from_excel(filepath):
    df = pd.read_excel(filepath)
    db = load_db()
    for _, row in df.iterrows():
        code = row.get("code") or secrets.token_hex(8)
        days = int(row.get("days", 30))
        db["licenses"].append({
            "code": code,
            "days": days,
            "used": False,
            "used_by": None,
            "issued_at": datetime.now().isoformat()
        })
    save_db(db)
    return len(df)

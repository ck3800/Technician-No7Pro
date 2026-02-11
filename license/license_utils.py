import json
import os
import time
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))
os.makedirs(DATA_DIR, exist_ok=True)

LICENSE_DB = os.path.join(DATA_DIR, "licenses.json")


def _ensure_db():
    if not os.path.exists(LICENSE_DB):
        with open(LICENSE_DB, "w", encoding="utf-8") as f:
            json.dump(
                {"activated": False, "license_key_sha256": "", "activated_at": 0},
                f,
                ensure_ascii=False,
                indent=2,
            )


def load_license():
    _ensure_db()
    with open(LICENSE_DB, "r", encoding="utf-8") as f:
        return json.load(f)


def save_license(data: dict):
    os.makedirs(os.path.dirname(LICENSE_DB), exist_ok=True)
    with open(LICENSE_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def activate_license(plain_key: str) -> bool:
    plain_key = (plain_key or "").strip()
    if not plain_key:
        return False
    data = load_license()
    sha = hashlib.sha256(plain_key.encode("utf-8")).hexdigest()
    data.update({"activated": True, "license_key_sha256": sha, "activated_at": int(time.time())})
    save_license(data)
    return True


def is_activated() -> bool:
    if os.environ.get("LICENSE_BYPASS") == "1":
        return True
    data = load_license()
    return bool(data.get("activated"))

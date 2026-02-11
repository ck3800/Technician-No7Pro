from datetime import datetime
import os

LOG_FILE = "auth/login.log"

def log_login(username, success=True):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {'✅' if success else '❌'} {username}\n")

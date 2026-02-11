import os
import json

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from auth import authenticate, User
from db import get_all_accounts
from sender import run_mass_send_web_group
from api.api_send import api
from admin.upload import admin
import scheduler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "task_log")
os.makedirs(LOG_DIR, exist_ok=True)

app = Flask(__name__)

# Ensure runtime dirs exist (Render upload may omit empty folders)
os.makedirs('task_log', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(admin)


@login_manager.user_loader
def load_user(user_id: str):
    return User(user_id)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(BASE_DIR, "static"), "favicon.ico")


# ---- Scheduler (optional) ----
if os.environ.get("DISABLE_SCHEDULER", "0") != "1":
    try:
        scheduler.schedule_group_send("groupA", hour=12, minute=0)
        scheduler.start()
    except Exception as e:
        # Avoid crashing the web service if scheduler can't start
        print(f"[scheduler] init failed: {e}")


# ---- Routes ----
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = authenticate(username, password)
        if user:
            login_user(user)
            next_url = request.args.get("next") or url_for("index")
            return redirect(next_url)
        error = "用户名或密码错误"
    return render_template("login.html", error=error, title="登录")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    accounts = get_all_accounts()
    return render_template("index.html", accounts=accounts, title="首页")


@app.route("/send/<group_name>")
@login_required
def send_group(group_name: str):
    # 注意：该函数目前仅写日志/占位。请勿用于骚扰或垃圾信息发送。
    run_mass_send_web_group(group_name)
    return redirect(url_for("history"))


@app.route("/history")
@login_required
def history():
    try:
        logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".json")], reverse=True)
    except FileNotFoundError:
        logs = []
    return render_template("history.html", logs=logs, title="任务日志")


@app.route("/download/<path:filename>")
@login_required
def download_log(filename: str):
    safe_path = os.path.abspath(os.path.join(LOG_DIR, filename))
    if not safe_path.startswith(os.path.abspath(LOG_DIR) + os.sep):
        abort(400)
    if not os.path.exists(safe_path):
        abort(404)
    return send_from_directory(LOG_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)

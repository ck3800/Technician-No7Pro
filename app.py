import os
import json

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from auth import authenticate, User
from db import get_all_accounts
from sender import run_mass_send_web_group
from api.api_send import api
from admin.upload import admin
from tg_login_routes import tg_bp

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'change-me-in-env')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure runtime directories exist
os.makedirs(os.path.join(BASE_DIR, 'task_log'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'accounts'), exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(tg_bp, url_prefix='/tg')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'favicon.ico')

# ---- Scheduler (optional) ----
if os.environ.get('DISABLE_SCHEDULER') != '1':
    try:
        import scheduler as _scheduler
        _scheduler.init(app)
        group_name = os.environ.get('DEFAULT_GROUP', 'groupA')
        hour = int(os.environ.get('SCHEDULE_HOUR', '12'))
        minute = int(os.environ.get('SCHEDULE_MINUTE', '0'))
        _scheduler.schedule_group_send(group_name=group_name, hour=hour, minute=minute)
        _scheduler.start()
        print(f"[scheduler] enabled: group={group_name} time={hour:02d}:{minute:02d} UTC")
    except Exception as e:
        # Avoid crashing the web service if scheduler can't start
        print(f"[scheduler] disabled due to error: {e}")

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



@app.get('/healthz')
def healthz():
    return {'ok': True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)

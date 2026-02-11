from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from auth import authenticate, User
from sender import run_mass_send_web_group
from db import get_all_accounts
import os, json
try:
    from api.api_send import api
except Exception as e:
    api = None
    print('WARN: api module not loaded:', e)
from admin.upload import admin
try:
    import scheduler
except Exception as e:
    scheduler = None
    print('WARN: scheduler not loaded:', e)

app = Flask(__name__)
import os
os.makedirs('task_log', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)
app.secret_key = 'super_secret_tech_007'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

if api:
    app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(admin)

scheduler.schedule_group_send("groupA", hour=12, minute=0)
scheduler.start()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = authenticate(request.form['username'], request.form['password'])
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="登录失败，请检查账号密码")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    log = None
    with open("config/groups.json", encoding="utf-8") as f:
        groups = list(json.load(f).keys())
    if request.method == 'POST':
        group_name = request.form['group']
        log = run_mass_send_web_group(group_name)
    status = get_all_accounts()
    return render_template('index.html', log=log, status=status, groups=groups)

@app.route("/history")
@login_required
def history():
    files = os.listdir("task_log")
    return render_template("history.html", history=files)

@app.route("/task_log/<filename>")
@login_required
def task_file(filename):
    return send_from_directory("task_log", filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
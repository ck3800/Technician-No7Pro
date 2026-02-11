
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from auth import authenticate, User
from sender import run_mass_send_web
from db import get_all_accounts
import os

app = Flask(__name__)
app.secret_key = 'super_secret_tech_007'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
    if request.method == 'POST':
        group = request.form['target']
        file = request.files['script']
        if file.filename:
            filepath = os.path.join('uploads', file.filename)
            file.save(filepath)
            log = run_mass_send_web(filepath, group)
    status = get_all_accounts()
    return render_template('index.html', log=log, status=status)

# ✅ This is the Render-compatible entry point
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

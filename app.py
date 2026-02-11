from flask import Flask, redirect, url_for
from flask_login import LoginManager
import scheduler

app = Flask(__name__)
app.secret_key = 'secret'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return "登录界面"

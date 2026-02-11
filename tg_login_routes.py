from flask import Blueprint

from flask import request, render_template, redirect
from login_tg import start_login, complete_login

def register_tg_login_routes(app):
    @app.route('/tglogin', methods=['GET', 'POST'])
    def tglogin():
        if request.method == 'POST':
            phone = request.form['phone']
            start_login(phone)
            return redirect('/tgcode')
        return render_template('tg_login.html')

    @app.route('/tgcode', methods=['GET', 'POST'])
    def tgcode():
        if request.method == 'POST':
            code = request.form['code']
            password = request.form.get('password')
            result = complete_login(code, password)
            return f"<pre>{result}</pre>"
        return render_template('tg_code.html')


# Compatibility: some deployments may import `tg_bp`; we keep a placeholder Blueprint.
tg_bp = Blueprint('tg_bp', __name__)

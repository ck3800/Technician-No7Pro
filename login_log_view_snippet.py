@app.route("/login_log")
def view_log():
    log_path = "auth/login.log"
    if not os.path.exists(log_path):
        return "暂无日志"
    with open(log_path, "r", encoding="utf-8") as f:
        return f"<pre>{f.read()}</pre>"

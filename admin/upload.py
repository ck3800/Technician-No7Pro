import os
from flask import Blueprint, request, render_template

admin = Blueprint("admin", __name__)

@admin.route("/upload", methods=["GET", "POST"])
def upload():
    msg = None
    if request.method == "POST":
        f = request.files.get("file")
        if f and f.filename:
            save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
            save_dir = os.path.abspath(save_dir)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f.filename)
            f.save(save_path)
            msg = f"上传成功：{f.filename}"
        else:
            msg = "请选择要上传的文件。"
    return render_template("upload.html", message=msg)

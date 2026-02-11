import os
from flask import Blueprint, request, redirect, render_template

admin = Blueprint("admin", __name__)

@admin.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files["file"]
        if f:
            save_dir = "uploads"
            os.makedirs(save_dir, exist_ok=True)
            f.save(os.path.join(save_dir, f.filename))
            return redirect("/upload")
    return render_template("upload.html")

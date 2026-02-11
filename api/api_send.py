from flask import Blueprint, request, jsonify
from sender import run_mass_send_web_group

api = Blueprint("api", __name__)

@api.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    group = data.get("group")
    result = run_mass_send_web_group(group)
    return jsonify({"log": result})

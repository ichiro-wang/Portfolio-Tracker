from flask import Blueprint, jsonify
from backend.flasktracker.models import User


users = Blueprint("users", __name__, url_prefix="/api/users")


@users.route("/", methods=["GET"])
def get_users():
    try:
        users_list = User.query.all()
        print(users_list)
        result = [user.to_json() for user in users_list]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

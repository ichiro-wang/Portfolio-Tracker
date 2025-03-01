from backend.flasktracker import db
from flask import Blueprint, request, jsonify
from backend.flasktracker.models import User


users = Blueprint('users', __name__, url_prefix="/api/users")


@users.route("/", methods=["GET"])
def get_users():
    try:
        users_list = User.query.all()
        print(users_list)
        result = [user.to_json() for user in users_list]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users.route("/create", methods=["POST"])
def create_user():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

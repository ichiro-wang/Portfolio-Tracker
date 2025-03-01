from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user

from backend.flasktracker.models import User
from backend.flasktracker import db

auth = Blueprint("auth", __name__, url_prefix="/api/auth")


# sign up a new user
# validate inputs
# check for duplicate email existing in database
@auth.route("/signup", methods=["POST"])
def signup():
    try:
        # retrieve form data
        data = request.json
        name: str = data.get("name")
        email: str = data.get("email")
        password: str = data.get("password")

        name = name.strip() if name else ""
        email = email.strip() if email else ""

        # validating inputs
        if " " in password:
            return jsonify({"error": "Password should not contain space"}), 400
        if len(password) < 8:
            return jsonify({"error": "Password should be at least 8 characters"}), 400
        if not name or not email:
            return jsonify({"error": "Missing data"}), 400

        # check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already registered. Please log in"}), 400

        # static method to hash password before storing in db
        hashed_password = User.set_password(password)

        # creating new user and adding to db
        new_user = User(name, email, hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_json()), 201
    except Exception as e:
        # rollback any changes if error
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# log in a user
# check if email exists
# verify hashed password
@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email: str = data.get("email")
        password: str = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing data"}), 400

        user: User = User.query.filter_by(email=email).first()
        if user and user.validate_password(password):
            # login_user from flask login package
            login_user(user, True)
            return jsonify(user.to_json()), 200
        return jsonify({"error": "Invalid credentials"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200

@auth.route("/me", methods=["GET"])
def me():
    if current_user.is_authenticated:
        return jsonify(current_user.to_json()), 200
    return jsonify({"error": "Not logged in"}), 401
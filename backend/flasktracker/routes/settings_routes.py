from typing import cast
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from flasktracker.models import User
from flasktracker import db
from flasktracker.utils.handle_image import handle_image
from firebase_admin import storage
from dotenv import load_dotenv
import os

load_dotenv()


settings = Blueprint("settings", __name__, url_prefix="/api/settings")
authenticated_user: User = cast(User, current_user)


"""
get simple user details to display in settings page
"""
@settings.route("/me", methods=["GET"])
@login_required
def get_me():
    return jsonify(authenticated_user.to_json()), 200


"""
allow user to update their name
"""
@settings.route("/update/name", methods=["POST"])
@login_required
def update_name():
    try:
        data: dict[str, str] = request.json
        name = data.get("name", "").strip()

        if not name:
            return jsonify({"error": "Invalid name"}), 400

        authenticated_user.name = name
        db.session.commit()

        return jsonify(authenticated_user.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


"""
receive an image file
shrink it using helper method
upload image to firebase and update link to new image
delete previous image from firebase
"""
@settings.route("/update/picture", methods=["POST"])
@login_required
def update_picture():
    try:
        # receive file
        received_image = request.files["image"]

        if not received_image:
            return jsonify({"error": "No file provided"}), 400

        # run through helper function
        image, storage_file_name, content_type = handle_image(received_image)

        # firebase
        bucket = storage.bucket()
        blob = bucket.blob(storage_file_name)
        blob.upload_from_file(image, content_type=content_type)
        blob.make_public()

        # need old link to delete from firebase
        old_profile_pic: str = authenticated_user.profile_pic

        # update image link
        authenticated_user.profile_pic = blob.public_url
        db.session.commit()

        if old_profile_pic != os.getenv("DEFAULT_PICTURE"):
            object_name = old_profile_pic.split("/")[-1]
            old_blob = bucket.blob(object_name)
            old_blob.delete()

        return jsonify(authenticated_user.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

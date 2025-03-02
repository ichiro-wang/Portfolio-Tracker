from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore
from flask_login import LoginManager  # type: ignore

from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

import firebase_admin  # type: ignore
from firebase_admin import credentials  # type: ignore

from flasktracker.config import Config

db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = None


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Not logged in"})


# path to firebase serviceAccountKey.json
backend_path = os.path.dirname(os.path.dirname(__file__))
service_account_path = os.path.join(backend_path, "serviceAccountKey.json")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # firebase
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(
        cred,
        {"storageBucket": f"{os.getenv("FIREBASE_PROJECT_ID")}.firebasestorage.app"},
    )

    from flasktracker.routes.auth_routes import auth
    from flasktracker.routes.settings_routes import settings

    app.register_blueprint(auth)
    app.register_blueprint(settings)

    return app

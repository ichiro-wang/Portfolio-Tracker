from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

load_dotenv()

import firebase_admin
from firebase_admin import credentials

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
    migrate = Migrate(app, db)

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
    from flasktracker.routes.portfolios_routes import portfolios
    from flasktracker.routes.stocks_routes import stocks
    from flasktracker.routes.transactions_routes import transactions
    from flasktracker.routes.settings_routes import settings

    app.register_blueprint(auth)
    app.register_blueprint(portfolios)
    app.register_blueprint(stocks)
    app.register_blueprint(transactions)
    app.register_blueprint(settings)

    return app

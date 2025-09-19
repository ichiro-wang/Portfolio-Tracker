from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

load_dotenv()

# import firebase_admin
# from firebase_admin import credentials

from flasktracker.config import Config

db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = None


# handle protected routes when not authorized
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Not logged in"}), 401


# path to firebase serviceAccountKey.json
backend_path = os.path.dirname(os.path.dirname(__file__))
service_account_path = os.path.join(backend_path, "serviceAccountKey.json")

# path to frontend dist folder
frontend_dist_folder = os.path.join(os.getcwd(), "..", "frontend", "dist")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db, command="migrate")

    cors.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # firebase set up
    # if not firebase_admin._apps:
    #     cred = credentials.Certificate(service_account_path)
    #     firebase_admin.initialize_app(
    #         cred,
    #         {
    #             "storageBucket": f"{os.getenv('FIREBASE_PROJECT_ID')}.firebasestorage.app"
    #         },
    #     )

    """
    serve static files from frontend dist folder
    this allows us to access the frontend
    @app.route("/", defaults={"filename": ""})
    @app.route("/<path:filename>")
    def index(filename):
        if not filename:
            filename = "index.html"
        filepath = os.path.join(frontend_dist_folder, filename)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return send_from_directory(frontend_dist_folder, filename)
        else:
            return send_from_directory(frontend_dist_folder, "index.html")
    """

    # importing route blueprints
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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore
from flask_login import LoginManager

from backend.flasktracker.config import Config

db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from backend.flasktracker.routes.auth_routes import auth
    from backend.flasktracker.routes.user_routes import users

    app.register_blueprint(auth)
    app.register_blueprint(users)

    return app

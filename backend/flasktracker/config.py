from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI_TESTING")
    TESTING: True
    SERVER_NAME = "localhost"
    WTF_CSRF_ENABLED = False

from flask.testing import FlaskClient
import pytest
from flask import Flask
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flasktracker import create_app, db
from flasktracker.models import User, Portfolio, Stock, Transaction, TransactionType
from flasktracker.config import TestConfig


@pytest.fixture(scope="function")
def app():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()

        password = User.hash_password("password123")
        test_user_1 = User(name="Test User", email="test@test.com", password=password)
        db.session.add(test_user_1)

        test_portfolio_1 = Portfolio(name="Test Portfolio 1", owner_id=1)
        db.session.add(test_portfolio_1)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="function")
def auth_client(app: Flask) -> FlaskClient:
    client = app.test_client()

    client.post(
        "/api/auth/login",
        json={
            "email": "test@test.com",
            "password": "password123",
        },
    )

    return client

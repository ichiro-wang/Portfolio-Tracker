from flask.testing import FlaskClient
from flasktracker.models import (
    Portfolio,
    Stock,
    Transaction,
    StockWrapper,
    TransactionType,
)
from flasktracker import db


# helper function to create some transactions for testing
# creates for user with id = 1 with portfolio of id = 1
def create_stock_transactions() -> int:
    stock_wrapper = StockWrapper(ticker="GOOGL")
    db.session.add(stock_wrapper)
    stock = Stock(ticker="GOOGL", wrapper_id=1, portfolio_id=1)
    db.session.add(stock)
    t_1 = Transaction(
        type=TransactionType("buy"),
        quantity=10,
        price=100,
        stock_id=1,
        date="2025-03-10 00:00:00",
    )
    t_2 = Transaction(
        type=TransactionType("sell"),
        quantity=5,
        price=120,
        stock_id=1,
        date="2025-03-16 00:00:00",
    )
    db.session.add(t_1)
    db.session.add(t_2)
    db.session.commit()

    return stock.id


# retrieve stock transactions
def test_get_stock_transactions(auth_client: FlaskClient):
    stock_id = create_stock_transactions()

    # use above id to retrieve its transactions
    response = auth_client.get(f"/api/stocks/{stock_id}")

    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    # expect array with at least 1 transaction
    assert len(data) > 0
    assert data[0]["type"] == "buy"
    assert data[0]["quantity"] == 10
    assert data[1]["type"] == "sell"
    assert data[1]["quantity"] == 5


# retrieve stock transactions of another user
def test_get_stock_transactions_invalid(client: FlaskClient):
    # signup a new user
    response = client.post(
        "/api/auth/signup",
        json={
            "name": "Name",
            "email": "name@test.com",
            "password": "password123",
        },
    )
    response = client.get("/api/auth/me")
    data: dict[str, any] = response.get_json()
    assert data["name"] == "Name"

    # this stock belongs to a different user
    stock_id = create_stock_transactions()

    # retrieve other user's stock
    # should not work
    response = client.get(f"/api/stocks/{stock_id}")

    assert response.status_code == 403
    data: dict[str, any] = response.get_json()
    assert "Invalid request" in data["error"]


def test_get_stock_transactions(auth_client: FlaskClient):
    stock_id = create_stock_transactions()

    # delete above stock id
    response = auth_client.delete(f"/api/stocks/delete/{stock_id}")
    assert response.status_code == 200
    # returns deleted stock id and its portfolio id
    data: dict[str, any] = response.get_json()
    assert data["deletedId"] == stock_id
    assert data["portfolioId"] == 1

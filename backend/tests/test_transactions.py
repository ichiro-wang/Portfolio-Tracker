from datetime import datetime, timedelta
from flask.testing import FlaskClient

today = (datetime.now()).strftime("%Y-%m-%d")
tomorrow = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")


# creating a transaction
def test_create_transaction(auth_client: FlaskClient):
    # create a new transaction
    response = auth_client.post(
        "/api/transactions/create",
        json={
            "portfolioId": 1,
            "ticker": "AAPL",
            "type": "buy",
            "quantity": 10.0,
            "price": 150.0,
            "date": today,
        },
    )

    assert response.status_code == 201
    data: dict[str, any] = response.get_json()
    assert data["type"] == "buy"
    assert data["quantity"] == 10
    assert data["price"] == 150.0
    assert data["stockId"] is not None


# create a transaction without inputting all fields
def test_create_transaction_missing_fields(auth_client: FlaskClient):
    # missing price, quantity, and date
    response = auth_client.post(
        "/api/transactions/create",
        json={"portfolioId": 1, "ticker": "AAPL", "type": "buy"},
    )

    assert response.status_code == 400
    data: dict[str, any] = response.get_json()
    assert "Missing data" in data["error"]


# create a transaction using an invalid date (future)
def test_create_transaction_future_date(auth_client: FlaskClient):
    response = auth_client.post(
        "/api/transactions/create",
        json={
            "portfolioId": 1,
            "ticker": "AAPL",
            "type": "buy",
            "quantity": 5,
            "price": 200.0,
            "date": tomorrow,
        },
    )

    assert response.status_code == 400
    data: dict[str, any] = response.get_json()
    assert "Transaction date cannot be in the future" in data["error"]


# getting a transaction
def test_get_transaction(auth_client: FlaskClient):
    # create a transaction first
    response = auth_client.post(
        "/api/transactions/create",
        json={
            "portfolioId": 1,
            "ticker": "TSLA",
            "type": "buy",
            "quantity": 3,
            "price": 700.0,
            "date": today,
        },
    )
    data: dict[str, any] = response.get_json()
    transaction_id = data["id"]

    # now retrieve the transaction
    response = auth_client.get(f"/api/transactions/{transaction_id}")

    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    assert data["id"] == transaction_id
    assert data["type"] == "buy"


# get a nonexistent transaction
def test_get_transaction_not_found(auth_client: FlaskClient):
    response = auth_client.get("/api/transactions/999999")
    assert response.status_code == 404
    data: dict[str, any] = response.get_json()
    assert "Transaction not found" in data["error"]


# delete a transaction
def test_delete_transaction(auth_client: FlaskClient):
    # create a transaction first
    response = auth_client.post(
        "/api/transactions/create",
        json={
            "portfolioId": 1,
            "ticker": "GOOGL",
            "type": "sell",
            "quantity": 2,
            "price": 2800.0,
            "date": today,
        },
    )
    data: dict[str, any] = response.get_json()
    transaction_id = data["id"]

    # now delete the transaction
    response = auth_client.delete(
        f"/api/transactions/delete/{transaction_id}", json={"portfolioId": 1}
    )

    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    assert data["deletedId"] == transaction_id


# delete transaction of another user
def test_delete_transaction_invalid(auth_client: FlaskClient):
    response = auth_client.delete(
        "/api/transactions/delete/999999",  # transaction id arbitrary here since portfolio is checked first
        json={"portfolioId": 2},  # portfolioId 2 does not exist in auth_client
    )

    assert response.status_code == 403
    data: dict[str, any] = response.get_json()
    assert "Invalid request" in data["error"]

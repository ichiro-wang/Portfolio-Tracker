from flasktracker.models import Portfolio, User
from flasktracker import db
from flask.testing import FlaskClient


# retrieve all portfolios that belong to auth'd user
def test_get_all_portfolios(auth_client: FlaskClient):
    response = auth_client.get("/api/portfolios/all")

    assert response.status_code == 200

    data: dict[str, any] = response.get_json()
    print(data)
    assert isinstance(data, list)
    assert len(data) == 1  # check conftest to see already created portfolios
    assert data[0]["name"] == "Test Portfolio 1"


# create a portfolio
def test_create_portfolio(auth_client: FlaskClient):
    response = auth_client.post(
        "/api/portfolios/create", json={"name": "New Portfolio"}
    )

    assert response.status_code == 201
    data: dict[str, any] = response.get_json()
    assert data["name"] == "New Portfolio"

    # verify added to db
    response = auth_client.get("/api/portfolios/all")
    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    assert len(data) == 2  # original length was 1. check conftest
    assert data[1]["name"] == "New Portfolio"


# get portfolio with id
def test_get_portfolio(auth_client: FlaskClient):
    # get all portfolios, then take first id
    response = auth_client.get("/api/portfolios/all")
    data: dict[str, any] = response.get_json()
    portfolio_id: int = data[0]["id"]

    # take the above id and check get portfolio route
    response = auth_client.get(f"/api/portfolios/{portfolio_id}")
    assert response.status_code == 200
    # returns "portfolio" and "stocks"
    data: dict[str, any] = response.get_json()
    assert data["portfolio"]["name"] == "Test Portfolio 1"
    assert "stocks" in data


# helper function to create a portfolio for a seperate user
def create_other_user_portfolio() -> Portfolio:
    other_user = User(
        name="LeBron James", email="lebronjames@lebronjames.com", password="password"
    )
    db.session.add(other_user)
    other_user_portfolio = Portfolio(name="other user portfolio", owner_id=2)
    db.session.add(other_user_portfolio)
    db.session.commit()
    return other_user_portfolio


# get a portfolio that doesnt belong to current user
def test_get_portfolio_invalid(auth_client: FlaskClient):
    # nonexistent portfolio
    response = auth_client.get("/api/portfolios/99999")
    assert response.status_code == 404
    data: dict[str, any] = response.get_json()
    assert "could not be found" in data["error"]

    other_user_portfolio = create_other_user_portfolio()

    # should not be able to get above portfolio with current user
    response = auth_client.get(f"/api/portfolios/{other_user_portfolio.id}")
    assert response.status_code == 403
    data: dict[str, any] = response.get_json()
    assert "Invalid request" in data["error"]


# delete a portfolio
def test_delete_portfolio(auth_client: FlaskClient):
    # get all portfolios, then take first id
    response = auth_client.get("/api/portfolios/all")
    data: dict[str, any] = response.get_json()
    portfolio_id: int = data[0]["id"]

    # delete above portfolio
    response = auth_client.delete(f"/api/portfolios/delete/{portfolio_id}")
    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    assert data["deletedId"] == portfolio_id


def test_delete_portfolio_invalid(auth_client: FlaskClient):
    # delete nonexistent portfolio
    response = auth_client.delete("/api/portfolios/delete/99999")
    assert response.status_code == 404
    data: dict[str, any] = response.get_json()
    assert "could not be found" in data["error"]

    # create portfolio for different user
    other_user_portfolio = create_other_user_portfolio()

    # delete other user's portfolio
    # should not work
    response = auth_client.delete(f"/api/portfolios/delete/{other_user_portfolio.id}")
    assert response.status_code == 403
    data: dict[str, any] = response.get_json()
    assert "Invalid request" in data["error"]

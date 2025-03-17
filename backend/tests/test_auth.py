from flask.testing import FlaskClient


# valid signup
def test_signup_success(client: FlaskClient):
    response = client.post(
        "/api/auth/signup",
        json={
            "name": "Name",
            "email": "name@test.com",
            "password": "password123",
        },
    )

    # expect 201 created, with user data
    assert response.status_code == 201
    data: dict[str, any] = response.get_json()
    assert data["name"] == "Name"
    assert data["email"] == "name@test.com"


# invalid signups
def test_signup_fail(client: FlaskClient):
    # missing password
    response = client.post(
        "/api/auth/signup", json={"name": "Name", "email": "name@test.com"}
    )
    assert response.status_code == 400
    data: dict[str, any] = response.get_json()
    assert "Password should be at least 8" in data["error"]

    # missing name
    response = client.post(
        "/api/auth/signup", json={"email": "name@test.com", "password": "password123"}
    )
    assert response.status_code == 400
    data: dict[str, any] = response.get_json()
    assert "Missing data" in data["error"]

    # existing email
    response = client.post(
        "/api/auth/signup",
        json={"name": "Name", "email": "test@test.com", "password": "password123"},
    )
    assert response.status_code == 400
    data: dict[str, any] = response.get_json()
    assert "Email already" in data["error"]


# valid login
def test_login_success(client: FlaskClient):
    response = client.post(
        "/api/auth/login", json={"email": "test@test.com", "password": "password123"}
    )
    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@test.com"


# invalid logins
def test_login_fail(client: FlaskClient):
    # bad email
    response = client.post(
        "/api/auth/login", json={"email": "fail@test.com", "password": "password123"}
    )
    assert response.status_code == 400
    data: dict[str, any] = response.get_json()
    assert "Invalid cred" in data["error"]

    # bad password
    response = client.post(
        "/api/auth/login", json={"email": "test@test.com", "password": "passwordbad"}
    )
    assert response.status_code == 400
    data: dict[str, any] = response.get_json()
    assert "Invalid cred" in data["error"]


# get current auth'd user
def test_get_me_authenticated(auth_client: FlaskClient):
    response = auth_client.get("/api/auth/me")
    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@test.com"


# get current auth'd user while not logged in
def test_get_me_unauthenticated(client: FlaskClient):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    data: dict[str, any] = response.get_json()
    assert "Not logged in" in data["error"]


def test_logout(auth_client: FlaskClient):
    # verify we are logged in
    response = auth_client.get("/api/auth/me")
    assert response.status_code == 200

    # logout
    response = auth_client.post("/api/auth/logout")
    assert response.status_code == 200

    # verify we are logged out
    response = auth_client.get("/api/auth/me")
    assert response.status_code == 401

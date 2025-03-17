from flask.testing import FlaskClient


# updating name
def test_update_name(auth_client: FlaskClient):
    response = auth_client.post("/api/settings/update/name", json={"name": "Joe"})
    assert response.status_code == 200
    data: dict[str, any] = response.get_json()
    assert data["name"] == "Joe"

import pytest


@pytest.fixture()
def created_user_details(client):
    username = "test_user"
    password = "test_password"
    client.post(
        "/register",
        json={"username": username, "password": password},
    )

    return username, password


def test_register_user(client):
    username = "test_user"
    response = client.post(
        "/register",
        json={"username": username, "password": "Test Password"},
    )

    assert response.status_code == 201
    assert response.json == {"message": "User created successfully."}


def test_register_user_already_exists(client):
    username = "test_user"
    client.post(
        "/register",
        json={"username": username, "password": "Test Password"},
    )

    response = client.post(
        "/register",
        json={"username": username, "password": "Test Password"},
    )

    assert response.status_code == 409
    assert response.json["message"] == "A user with that username already exists."


def test_register_user_missing_data(client):
    response = client.post(
        "/register",
        json={},
    )

    assert response.status_code == 422
    assert "password" in response.json["errors"]["json"]
    assert "username" in response.json["errors"]["json"]


def test_get_user_details(client, created_user_details):
    response = client.get(
        "/user/1",  # assume user id is 1
    )

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "username": created_user_details[0],
    }


def test_get_user_details_missing(client):
    response = client.get(
        "/user/23",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}

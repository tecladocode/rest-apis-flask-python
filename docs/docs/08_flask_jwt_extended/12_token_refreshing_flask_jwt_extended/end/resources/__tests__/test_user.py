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


@pytest.fixture()
def created_user_jwts(client, created_user_details):
    username, password = created_user_details
    response = client.post(
        "/login",
        json={"username": username, "password": password},
    )

    return response.json["access_token"], response.json["refresh_token"]


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


def test_login_user(client, created_user_details):
    username, password = created_user_details
    response = client.post(
        "/login",
        json={"username": username, "password": password},
    )

    assert response.status_code == 200
    assert response.json["access_token"]


def test_login_user_bad_password(client, created_user_details):
    username, _ = created_user_details
    response = client.post(
        "/login",
        json={"username": username, "password": "bad_password"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "Invalid credentials."


def test_login_user_bad_username(client, created_user_details):
    _, password = created_user_details
    response = client.post(
        "/login",
        json={"username": "bad_username", "password": password},
    )

    assert response.status_code == 401
    assert response.json["message"] == "Invalid credentials."


def test_logout_user(client, created_user_jwts):
    response = client.post(
        "/logout",
        headers={"Authorization": f"Bearer {created_user_jwts[0]}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Successfully logged out"


def test_logout_user_twice(client, created_user_jwts):
    client.post(
        "/logout",
        headers={"Authorization": f"Bearer {created_user_jwts[0]}"},
    )
    response = client.post(
        "/logout",
        headers={"Authorization": f"Bearer {created_user_jwts[0]}"},
    )

    assert response.status_code == 401
    assert response.json == {
        "description": "The token has been revoked.",
        "error": "token_revoked",
    }


def test_logout_user_no_token(client):
    response = client.post(
        "/logout",
    )

    assert response.status_code == 401
    assert response.json["description"] == "Request does not contain an access token."


def test_logout_user_invalid_token(client):
    response = client.post(
        "/logout",
        headers={"Authorization": "Bearer bad_token"},
    )

    assert response.status_code == 401
    assert response.json == {
        "error": "invalid_token",
        "message": "Signature verification failed.",
    }


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


def test_refresh_token_invalid(client):
    response = client.post(
        "/refresh",
        headers={"Authorization": "Bearer bad_jwt"},
    )

    assert response.status_code == 401


def test_refresh_token(client, created_user_jwts):
    response = client.post(
        "/refresh",
        headers={"Authorization": f"Bearer {created_user_jwts[1]}"},
    )

    assert response.status_code == 200
    assert response.json["access_token"]


def test_refresh_token_twice(client, created_user_jwts):
    client.post(
        "/refresh",
        headers={"Authorization": f"Bearer {created_user_jwts[1]}"},
    )
    response = client.post(
        "/refresh",
        headers={"Authorization": f"Bearer {created_user_jwts[1]}"},
    )

    assert response.status_code == 401
    assert response.json == {
        "description": "The token has been revoked.",
        "error": "token_revoked",
    }

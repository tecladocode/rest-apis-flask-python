import pytest


@pytest.fixture()
def created_store_id(client):
    response = client.post(
        "/stores",
        json={"name": "Test Store"},
    )

    return response.json["id"]


@pytest.fixture()
def created_item_id(client, fresh_jwt, created_store_id):
    response = client.post(
        "/items",
        json={"name": "Test Item", "price": 10.5, "store_id": created_store_id},
        headers={"Authorization": f"Bearer {fresh_jwt}"},
    )

    return response.json["id"]


@pytest.fixture()
def created_tag_id(client, created_store_id):
    response = client.post(
        f"/stores/{created_store_id}/tags",
        json={"name": "Test Tag"},
    )

    return response.json["id"]

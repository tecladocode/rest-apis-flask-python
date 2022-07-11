def test_get_store(client, created_store_id):
    response = client.get(
        f"/store/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "name": "Test Store",
        "items": [],
        "tags": [],
    }


def test_get_store_not_found(client):
    response = client.get(
        "/store/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_get_store_with_item(client, created_store_id):
    client.post(
        "/item",
        json={"name": "Test Item", "price": 10.5, "store_id": created_store_id},
    )

    response = client.get(
        f"/store/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["items"] == [
        {
            "id": 1,
            "name": "Test Item",
            "price": 10.5,
        }
    ]


def test_get_store_with_tag(client, created_store_id):
    client.post(
        f"/store/{created_store_id}/tag",
        json={"name": "Test Tag"},
    )

    response = client.get(
        f"/store/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["tags"] == [{"id": 1, "name": "Test Tag"}]


def test_create_store(client):
    response = client.post(
        "/store",
        json={"name": "Test Store"},
    )

    assert response.status_code == 201
    assert response.json["name"] == "Test Store"


def test_create_store_with_items(client, created_store_id):
    client.post(
        "/item",
        json={"name": "Test Item", "price": 10.5, "store_id": 1},
    )

    # Get the store with id 1 and check the items contains the newly created item
    response = client.get(
        f"/store/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json["items"] == [
        {
            "id": 1,
            "name": "Test Item",
            "price": 10.5,
        }
    ]


def test_delete_store(client, created_store_id):
    response = client.delete(
        f"/store/{created_store_id}",
    )

    assert response.status_code == 200
    assert response.json == {"message": "Store deleted"}


def test_delete_store_doesnt_exist(client):
    response = client.delete(
        "/store/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_get_store_list_empty(client):
    response = client.get(
        "/store",
    )

    assert response.status_code == 200
    assert response.json == []


def test_get_store_list_single(client):
    client.post(
        "/store",
        json={"name": "Test Store"},
    )

    response = client.get(
        "/store",
    )

    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "Test Store", "items": [], "tags": []}]


def test_get_store_list_multiple(client):
    client.post(
        "/store",
        json={"name": "Test Store"},
    )
    client.post(
        "/store",
        json={"name": "Test Store 2"},
    )

    response = client.get(
        "/store",
    )

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "name": "Test Store", "items": [], "tags": []},
        {"id": 2, "name": "Test Store 2", "items": [], "tags": []},
    ]


def test_get_store_list_with_items(client):
    client.post(
        "/store",
        json={"name": "Test Store"},
    )
    client.post(
        "/item",
        json={"name": "Test Item", "price": 10.5, "store_id": 1},
    )

    response = client.get(
        "/store",
    )

    assert response.status_code == 200
    assert response.json == [
        {
            "id": 1,
            "name": "Test Store",
            "items": [
                {
                    "id": 1,
                    "name": "Test Item",
                    "price": 10.5,
                }
            ],
            "tags": [],
        }
    ]


def test_get_store_list_with_tags(client):
    resp = client.post(
        "/store",
        json={"name": "Test Store"},
    )
    client.post(
        f"/store/{resp.json['id']}/tag",
        json={"name": "Test Tag"},
    )
    response = client.get(
        "/store",
    )

    assert response.status_code == 200
    assert response.json == [
        {
            "id": 1,
            "name": "Test Store",
            "items": [],
            "tags": [{"id": 1, "name": "Test Tag"}],
        }
    ]


def test_create_store_duplicate_name(client):
    client.post(
        "/store",
        json={"name": "Test Store"},
    )

    response = client.post(
        "/store",
        json={"name": "Test Store"},
    )
    assert response.status_code == 400
    assert response.json["message"] == "A store with that name already exists."

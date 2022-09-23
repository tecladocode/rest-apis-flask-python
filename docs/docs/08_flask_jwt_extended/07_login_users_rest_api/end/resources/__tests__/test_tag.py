import pytest
import logging

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def created_tag_with_item_id(client, created_item_id, created_tag_id):
    client.post(f"/item/{created_item_id}/tag/{created_tag_id}")

    response = client.get(
        f"/tag/{created_tag_id}",
    )

    return response.json["id"]


def test_get_tag(client, created_tag_id):
    response = client.get(
        f"/tag/{created_tag_id}",
    )

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "name": "Test Tag",
        "items": [],
        "store": {"id": 1, "name": "Test Store"},
    }


def test_get_tag_not_found(client):
    response = client.get(
        "/tag/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_items_linked_with_tag(client, created_tag_with_item_id):
    response = client.get(
        f"/tag/{created_tag_with_item_id}",
    )

    assert response.status_code == 200
    assert response.json["items"] == [
        {
            "id": 1,
            "name": "Test Item",
            "price": 10.5,
        }
    ]


def test_unlink_tag_from_item(client, created_item_id, created_tag_with_item_id):
    client.delete(f"/item/{created_item_id}/tag/{created_tag_with_item_id}")

    response = client.get(
        f"/tag/{created_tag_with_item_id}",
    )

    assert response.status_code == 200
    assert response.json["items"] == []


def test_delete_tag_without_items(client, created_tag_id):
    delete_response = client.delete(f"/tag/{created_tag_id}")

    response = client.get(
        f"/tag/{created_tag_id}",
    )

    assert delete_response.status_code == 202

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_delete_tag_still_has_items(client, created_tag_with_item_id):
    response = client.delete(f"/tag/{created_tag_with_item_id}")

    assert response.status_code == 400
    assert (
        response.json["message"]
        == "Could not delete tag. Make sure tag is not associated with any items, then try again."
    )


def test_delete_tag_not_found(client):
    response = client.delete(
        "/tag/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_get_all_tags_in_store(client, created_store_id, created_tag_id):
    response = client.get(
        f"/store/{created_store_id}/tag",
    )

    assert response.status_code == 200
    assert response.json == [
        {
            "id": created_tag_id,
            "name": "Test Tag",
            "items": [],
            "store": {"id": 1, "name": "Test Store"},
        }
    ]


def test_get_all_tags_in_store_not_found(client):
    response = client.get(
        "/store/1/tag",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}

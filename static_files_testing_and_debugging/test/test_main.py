from fastapi.testclient import TestClient
from static_files_testing_and_debugging.main import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "wrong"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid x-token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Bartender"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Bartender",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "badheader"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the Bazz"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid x-token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foo", "title": "Bazz", "description": "Drop the Bazz"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Item already exists"}

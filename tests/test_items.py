import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app


@pytest.fixture(autouse=True)
def limpiar_items() -> None:
    main._items.clear()
    main._next_id = 1


client = TestClient(app)


def test_item_get() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_item_post() -> None:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}


def test_item_get_by_id() -> None:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}

    response = client.get(f"/items/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}


def test_item_delete() -> None:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}

    response = client.delete(f"/items/{response.json()['id']}")
    assert response.status_code == 204
    assert response.content == b''


def test_item_update() -> None:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}

    response = client.put(f"/items/{response.json()['id']}", json={"name": "Test Item Updated", "price": 86.0})
    
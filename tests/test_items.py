import pytest
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def limpiar_items() -> None:
    main._items.clear()
    main._next_id = 1


@pytest.fixture()
def crear_items() -> dict:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0})
    return response.json()


def test_item_get() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_item_get_by_id(crear_items: dict) -> None:
    response = client.get(f"/items/{crear_items['id']}")
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}


def test_item_get_by_id_not_found() -> None:
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item no encontrado"}


def test_item_post() -> None:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}


def test_item_post_negative() -> None:
    response = client.post("/items", json={"name": "Test Negative", "price": -86.0})
    assert response.status_code == 422


def test_item_update(crear_items: dict) -> None:
    response = client.put(
        f"/items/{crear_items['id']}", json={"name": "Test Item Updated", "price": 86.0}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item Updated", "price": 86.0, "id": 1}

    response = client.get(f"/items/{crear_items['id']}")
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item Updated", "price": 86.0, "id": 1}


def test_item_update_negative() -> None:
    response = client.put(
        "/items/1", json={"name": "Test Item Updated", "price": -86.0}
    )
    assert response.status_code == 422


def test_item_update_not_found() -> None:
    response = client.put(
        "/items/999", json={"name": "Test Item Updated", "price": 86.0}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item no encontrado"}


def test_item_delete(crear_items: dict) -> None:
    response = client.delete(f"/items/{crear_items['id']}")
    assert response.status_code == 204
    assert response.content == b""

    response = client.get(f"/items/{crear_items['id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item no encontrado"}


def test_item_delete_not_found() -> None:
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item no encontrado"}

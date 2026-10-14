import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app


@pytest.fixture(autouse=True)
def limpiar_items() -> None:
    main._items.clear()
    main._next_id = 1

@pytest.fixture(autouse=False)
def crear_item() -> int:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0, "name": "Test Item2", "price": 86.0})

client = TestClient(app)


def test_item_get() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_item_post() -> None:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": 1}


def test_get_item(crear_item: int) -> None:
    response = client.get(f"/items/{crear_item}")
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item", "price": 74.0, "id": crear_item}
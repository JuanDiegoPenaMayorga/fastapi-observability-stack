from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_item_get() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_item_post() -> None:
    response = client.post("/items", json={"name": "Test Item", "price": 74.0}, )
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "price": 74.0,"id": 1 }

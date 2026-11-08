from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_metrics_responde() -> None:
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_metrics_cuenta_errores() -> None:
    client.get("/items/999999")  # no existe, da 404
    response = client.get("/metrics")
    assert (
        'http_errors_total{method="GET",path="/items/{item_id}",status="404"}'
        in response.text
    )

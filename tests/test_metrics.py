from fastapi.testclient import TestClient
from prometheus_client import REGISTRY

from app.main import app

client = TestClient(app)


@app.get("/boom")
def boom() -> None:
    raise RuntimeError("Controled Boom!")


def test_metrics_response() -> None:
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_metrics_error_count() -> None:
    client.get("/items/999999")
    response = client.get("/metrics")
    assert (
        'http_errors_total{method="GET",path="/items/{item_id}",status="404"}'
        in response.text
    )


def test_metrics_count_500() -> None:
    labels = {"method": "GET", "path": "/boom", "status": "500"}
    antes = REGISTRY.get_sample_value("http_errors_total", labels) or 0

    c = TestClient(app, raise_server_exceptions=False)
    assert c.get("/boom").status_code == 500

    despues = REGISTRY.get_sample_value("http_errors_total", labels)
    assert despues == antes + 1

def test_metrics_not_self_counting() -> None:
    client.get("/metrics")
    text = client.get("/metrics").text
    assert 'path="/metrics"' not in text

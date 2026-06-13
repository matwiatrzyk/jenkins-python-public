"""HTTP-layer tests using TestClient (based on httpx)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_vat_endpoint():
    response = client.get("/vat", params={"net": 100, "rate": 23})
    assert response.status_code == 200
    assert response.json()["gross"] == 123.0


def test_vat_negative_returns_400():
    response = client.get("/vat", params={"net": -5})
    assert response.status_code == 400

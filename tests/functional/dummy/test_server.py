from fastapi.testclient import TestClient

from app.services.dummy.server import app

client = TestClient(app)


def test_get_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "") == "text/plain; charset=utf-8"
    assert response.text == "OK"

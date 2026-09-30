from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_validation_error():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid-email",
            "password": "test"
        }
    )
    assert response.status_code == 422
    


def test_unauthorized_request():
    response = client.get("/api/v1/doctors")
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_invalid_login():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "notfound@example.com",
            "password": "Wrong@123"
        }
    )
    assert response.status_code == 401
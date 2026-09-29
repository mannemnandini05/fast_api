from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "Test@123",
            "role": "doctor",
        },
    )

    assert response.status_code in [200, 400]


def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@example.com",
            "password": "Wrong@123",
        },
    )

    assert response.status_code == 401
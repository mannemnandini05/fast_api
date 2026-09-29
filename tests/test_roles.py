from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_unauthorized_doctor_delete():
    response = client.delete("/api/v1/doctors/999999")

    assert response.status_code == 401


def test_unauthorized_patient_delete():
    response = client.delete("/api/v1/patients/999999")

    assert response.status_code == 401
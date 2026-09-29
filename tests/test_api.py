from datetime import datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def create_admin_and_get_token():
    email = f"admin_{uuid4().hex[:8]}@example.com"
    password = "Admin@123"

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "role": "admin"
        }
    )

    assert register_response.status_code in [200,201]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert login_response.status_code in [200,201]

    return login_response.json()["access_token"]


def test_admin_doctor_patient_appointment_flow():
    token = create_admin_and_get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    doctor_email = f"doctor_{uuid4().hex[:8]}@example.com"

    doctor_response = client.post(
        "/api/v1/doctors",
        json={
            "name": "Test Doctor",
            "specialization": "Cardiology",
            "email": doctor_email
        },
        headers=headers
    )

    assert doctor_response.status_code in [200,201]
    doctor_id = doctor_response.json()["id"]

    doctor_list_response = client.get(
        "/api/v1/doctors",
        headers=headers
    )

    assert doctor_list_response.status_code in [200,201]

    doctor_get_response = client.get(
        f"/api/v1/doctors/{doctor_id}",
        headers=headers
    )

    assert doctor_get_response.status_code in [200,201]

    patient_response = client.post(
        "/api/v1/patients",
        json={
            "name": "Test Patient",
            "age": 30,
            "phone": "9876543210"
        },
        headers=headers
    )

    assert patient_response.status_code in [200,201]
    patient_id = patient_response.json()["id"]

    assign_response = client.post(
        f"/api/v1/doctors/{doctor_id}/patients/{patient_id}",
        headers=headers
    )

    assert assign_response.status_code in [200,201]

    doctor_patients_response = client.get(
        f"/api/v1/doctors/{doctor_id}/patients",
        headers=headers
    )

    assert doctor_patients_response.status_code in [200,201]

    appointment_date = (
        datetime.now() + timedelta(days=10)
    ).replace(microsecond=0).isoformat()

    appointment_response = client.post(
        "/api/v1/appointments",
        json={
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "appointment_date": appointment_date,
            "status": "scheduled"
        },
        headers=headers
    )

    assert appointment_response.status_code in  [200,201]
    appointment_id = appointment_response.json()["id"]

    appointment_get_response = client.get(
        f"/api/v1/appointments/{appointment_id}",
        headers=headers
    )

    assert appointment_get_response.status_code in [200,201]

    doctor_appointments_response = client.get(
        f"/api/v1/doctors/{doctor_id}/appointments",
        headers=headers
    )

    assert doctor_appointments_response.status_code in [200,201]

    patient_appointments_response = client.get(
        f"/api/v1/patients/{patient_id}/appointments",
        headers=headers
    )

    assert patient_appointments_response.status_code in [200,201]

    appointment_update_response = client.put(
        f"/api/v1/appointments/{appointment_id}",
        json={
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "appointment_date": appointment_date,
            "status": "completed"
        },
        headers=headers
    )

    assert appointment_update_response.status_code in [200,201]

    appointment_delete_response = client.delete(
        f"/api/v1/appointments/{appointment_id}",
        headers=headers
    )

    assert appointment_delete_response.status_code in  [200,201]


def test_admin_patient_get_and_update():
    token = create_admin_and_get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    patient_response = client.post(
        "/api/v1/patients",
        json={
            "name": "Update Patient",
            "age": 25,
            "phone": "9876543210"
        },
        headers=headers
    )

    assert patient_response.status_code in [200,201]
    patient_id = patient_response.json()["id"]

    get_response = client.get(
        f"/api/v1/patients/{patient_id}",
        headers=headers
    )

    assert get_response.status_code in [200,201]

    update_response = client.put(
        f"/api/v1/patients/{patient_id}",
        json={
            "name": "Updated Patient",
            "age": 26,
            "phone": "9876543211"
        },
        headers=headers
    )

    assert update_response.status_code in  [200,201]


def test_unauthorized_access():
    response = client.get("/api/v1/doctors")

    assert response.status_code == 401


def test_invalid_patient_age():
    token = create_admin_and_get_token()

    response = client.post(
        "/api/v1/patients",
        json={
            "name": "Invalid Patient",
            "age": 0,
            "phone": "9876543210"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422
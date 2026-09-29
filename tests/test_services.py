from models import Doctor, Patient


def test_doctor_model_fields():
    doctor = Doctor(
        name="Test Doctor",
        specialization="Cardiology",
        email="doctor@test.com",
    )

    assert doctor.name == "Test Doctor"
    assert doctor.specialization == "Cardiology"
    assert doctor.email == "doctor@test.com"


def test_patient_model_fields():
    patient = Patient(
        name="Test Patient",
        age=25,
        phone="9876543210",
    )

    assert patient.name == "Test Patient"
    assert patient.age == 25
    assert patient.phone == "9876543210"
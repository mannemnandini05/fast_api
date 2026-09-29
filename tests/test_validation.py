import pytest
from pydantic import ValidationError

from schemas import PatientCreate


def test_valid_patient_phone():
    patient = PatientCreate(
        name="swami",
        age=22,
        phone="6302969760",
    )

    assert patient.phone == "6302969760"


def test_phone_less_than_10_digits():
    with pytest.raises(ValidationError):
        PatientCreate(
            name="swami",
            age=30,
            phone="876564689",
        )


def test_phone_more_than_15_digits():
    with pytest.raises(ValidationError):
        PatientCreate(
            name="swami",
            age=30,
            phone="1234567890123456",
        )


def test_invalid_age():
    with pytest.raises(ValidationError):
        PatientCreate(
            name="swami",
            age=0,
            phone="9876543210",
        )
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from models import Appointment, Doctor, Patient


# =========================================================
# DOCTOR SERVICES
# =========================================================

def create_doctor(
    db: Session,
    name: str,
    specialization: str,
    email: str,
    user_id: Optional[int] = None,
):
    existing_doctor = (
        db.query(Doctor)
        .filter(Doctor.email == email)
        .first()
    )

    if existing_doctor:
        return None

    doctor = Doctor(
        name=name,
        specialization=specialization,
        email=email,
        created_by=user_id,
        updated_by=user_id,
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


def get_doctors(
    db: Session,
    specialization=None,
    is_active=None,
    page=1,
    limit=10,
):
    query = db.query(Doctor)

    if specialization is not None:
        query = query.filter(
            Doctor.specialization == specialization
        )

    if is_active is not None:
        query = query.filter(
            Doctor.is_active == is_active
        )

    total = query.count()

    doctors = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return total, doctors


def get_doctor(db: Session, doctor_id: int):
    return (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )


def get_doctor_patients(
    db: Session,
    doctor_id: int,
):
    return (
        db.query(Patient)
        .filter(Patient.doctor_id == doctor_id)
        .all()
    )


def update_doctor(
    db: Session,
    doctor_id: int,
    name: str,
    specialization: str,
    email: str,
    user_id: Optional[int] = None,
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None, "Doctor not found"

    existing_doctor = (
        db.query(Doctor)
        .filter(
            Doctor.email == email,
            Doctor.id != doctor_id,
        )
        .first()
    )

    if existing_doctor:
        return None, "Doctor email already exists"

    doctor.name = name
    doctor.specialization = specialization
    doctor.email = email

    if user_id is not None:
        doctor.updated_by = user_id

    db.commit()
    db.refresh(doctor)

    return doctor, None


def patch_doctor(
    db: Session,
    doctor_id: int,
    name=None,
    specialization=None,
    email=None,
    user_id: Optional[int] = None,
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None, "Doctor not found"

    if email is not None:
        existing_doctor = (
            db.query(Doctor)
            .filter(
                Doctor.email == email,
                Doctor.id != doctor_id,
            )
            .first()
        )

        if existing_doctor:
            return None, "Doctor email already exists"

        doctor.email = email

    if name is not None:
        doctor.name = name

    if specialization is not None:
        doctor.specialization = specialization

    if user_id is not None:
        doctor.updated_by = user_id

    db.commit()
    db.refresh(doctor)

    return doctor, None


def delete_doctor(
    db: Session,
    doctor_id: int,
    user_id: Optional[int] = None,
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None

    doctor.is_active = False

    if user_id is not None:
        doctor.updated_by = user_id

    db.commit()
    db.refresh(doctor)

    return doctor


# =========================================================
# PATIENT SERVICES
# =========================================================

def create_patient(
    db: Session,
    name: str,
    age: int,
    phone: str,
    doctor_id=None,
    user_id: Optional[int] = None,
):
    if doctor_id is not None:
        doctor = get_doctor(db, doctor_id)

        if not doctor:
            return None, "Doctor not found"

        if not doctor.is_active:
            return None, "Doctor is inactive"

    patient = Patient(
        name=name,
        age=age,
        phone=phone,
        doctor_id=doctor_id,
        created_by=user_id,
        updated_by=user_id,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient, None


def get_patients(
    db: Session,
    age_gt=None,
    page=1,
    limit=10,
):
    query = db.query(Patient)

    if age_gt is not None:
        query = query.filter(
            Patient.age > age_gt
        )

    total = query.count()

    patients = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return total, patients


def get_patient(
    db: Session,
    patient_id: int,
):
    return (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )


def update_patient(
    db: Session,
    patient_id: int,
    name: str,
    age: int,
    phone: str,
    doctor_id=None,
    user_id: Optional[int] = None,
):
    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"

    if doctor_id is not None:
        doctor = get_doctor(db, doctor_id)

        if not doctor:
            return None, "Doctor not found"

        if not doctor.is_active:
            return None, "Doctor is inactive"

    patient.name = name
    patient.age = age
    patient.phone = phone
    patient.doctor_id = doctor_id

    if user_id is not None:
        patient.updated_by = user_id

    db.commit()
    db.refresh(patient)

    return patient, None


def patch_patient(
    db: Session,
    patient_id: int,
    name=None,
    age=None,
    phone=None,
    doctor_id=None,
    user_id: Optional[int] = None,
):
    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"

    if doctor_id is not None:
        doctor = get_doctor(db, doctor_id)

        if not doctor:
            return None, "Doctor not found"

        if not doctor.is_active:
            return None, "Doctor is inactive"

        patient.doctor_id = doctor_id

    if name is not None:
        patient.name = name

    if age is not None:
        patient.age = age

    if phone is not None:
        patient.phone = phone

    if user_id is not None:
        patient.updated_by = user_id

    db.commit()
    db.refresh(patient)

    return patient, None


def delete_patient(
    db: Session,
    patient_id: int,
):
    patient = get_patient(db, patient_id)

    if not patient:
        return None

    db.delete(patient)
    db.commit()

    return patient


# =========================================================
# DOCTOR-PATIENT ASSIGNMENT
# =========================================================

def assign_patient_to_doctor(
    db: Session,
    doctor_id: int,
    patient_id: int,
    user_id: Optional[int] = None,
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None, "Doctor not found"

    if not doctor.is_active:
        return None, "Doctor is inactive"

    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"

    patient.doctor_id = doctor_id

    if user_id is not None:
        patient.updated_by = user_id

    db.commit()
    db.refresh(patient)

    return patient, None


# =========================================================
# APPOINTMENT SERVICES
# =========================================================

def create_appointment(
    db: Session,
    doctor_id: int,
    patient_id: int,
    appointment_date: datetime,
    status: str,
    user_id: Optional[int] = None,
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None, "Doctor not found"

    if not doctor.is_active:
        return None, "Doctor is inactive"

    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"

    if patient.doctor_id != doctor_id:
        return None, "Patient is not assigned to this doctor"

    existing_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date,
        )
        .first()
    )

    if existing_appointment:
        return None, "Appointment overlaps with an existing appointment"

    appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_date=appointment_date,
        status=status,
        created_by=user_id,
        updated_by=user_id,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment, None


def get_appointments(db: Session):
    return (
        db.query(Appointment)
        .order_by(Appointment.appointment_date)
        .all()
    )


def get_appointment(
    db: Session,
    appointment_id: int,
):
    return (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )


def update_appointment(
    db: Session,
    appointment_id: int,
    doctor_id: int,
    patient_id: int,
    appointment_date: datetime,
    status: str,
    user_id: Optional[int] = None,
):
    appointment = get_appointment(
        db,
        appointment_id,
    )

    if not appointment:
        return None, "Appointment not found"

    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None, "Doctor not found"

    if not doctor.is_active:
        return None, "Doctor is inactive"

    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"

    if patient.doctor_id != doctor_id:
        return None, "Patient is not assigned to this doctor"

    existing_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date,
            Appointment.id != appointment_id,
        )
        .first()
    )

    if existing_appointment:
        return None, "Appointment overlaps with an existing appointment"

    appointment.doctor_id = doctor_id
    appointment.patient_id = patient_id
    appointment.appointment_date = appointment_date
    appointment.status = status

    if user_id is not None:
        appointment.updated_by = user_id

    db.commit()
    db.refresh(appointment)

    return appointment, None


def delete_appointment(
    db: Session,
    appointment_id: int,
):
    appointment = get_appointment(
        db,
        appointment_id,
    )

    if not appointment:
        return None

    db.delete(appointment)
    db.commit()

    return appointment


def get_doctor_appointments(
    db: Session,
    doctor_id: int,
):
    return (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .order_by(Appointment.appointment_date)
        .all()
    )


def get_patient_appointments(
    db: Session,
    patient_id: int,
):
    return (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .order_by(Appointment.appointment_date)
        .all()
    )
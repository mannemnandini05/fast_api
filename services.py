from sqlalchemy.orm import Session

from models import Doctor, Patient


def create_doctor(db: Session, name: str, specialization: str, email: str):
    existing_doctor = db.query(Doctor).filter(
        Doctor.email == email
    ).first()

    if existing_doctor:
        return None

    doctor = Doctor(
        name=name,
        specialization=specialization,
        email=email
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
    limit=10
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

    doctors = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return total, doctors


def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()


def get_doctor_patients(db: Session, doctor_id: int):
    return db.query(Patient).filter(
        Patient.doctor_id == doctor_id
    ).all()
def create_patient(
    db: Session,
    name: str,
    age: int,
    phone: str,
    doctor_id=None
):
    if doctor_id is not None:
        doctor = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()

        if not doctor:
            return None, "Doctor not found"

        if not doctor.is_active:
            return None, "Doctor is inactive"

    patient = Patient(
        name=name,
        age=age,
        phone=phone,
        doctor_id=doctor_id
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient, None


def get_patients(
    db: Session,
    age_gt=None,
    page=1,
    limit=10
):
    query = db.query(Patient)

    if age_gt is not None:
        query = query.filter(
            Patient.age > age_gt
        )

    total = query.count()

    patients = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return total, patients


def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(
        Patient.id == patient_id
    ).first()
def update_doctor(
    db: Session,
    doctor_id: int,
    name: str,
    specialization: str,
    email: str
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None, "Doctor not found"

    existing_doctor = db.query(Doctor).filter(
        Doctor.email == email,
        Doctor.id != doctor_id
    ).first()

    if existing_doctor:
        return None, "Doctor email already exists"

    doctor.name = name
    doctor.specialization = specialization
    doctor.email = email

    db.commit()
    db.refresh(doctor)

    return doctor, None


def patch_doctor(
    db: Session,
    doctor_id: int,
    name=None,
    specialization=None,
    email=None
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None, "Doctor not found"

    if email is not None:
        existing_doctor = db.query(Doctor).filter(
            Doctor.email == email,
            Doctor.id != doctor_id
        ).first()

        if existing_doctor:
            return None, "Doctor email already exists"

        doctor.email = email

    if name is not None:
        doctor.name = name

    if specialization is not None:
        doctor.specialization = specialization

    db.commit()
    db.refresh(doctor)

    return doctor, None


def delete_doctor(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return None

    doctor.is_active = False

    db.commit()
    db.refresh(doctor)

    return doctor
def update_patient(
    db: Session,
    patient_id: int,
    name: str,
    age: int,
    phone: str,
    doctor_id=None
):
    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"

    if doctor_id is not None:
        doctor = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()

        if not doctor:
            return None, "Doctor not found"

        if not doctor.is_active:
            return None, "Doctor is inactive"

    patient.name = name
    patient.age = age
    patient.phone = phone
    patient.doctor_id = doctor_id

    db.commit()
    db.refresh(patient)

    return patient, None


def patch_patient(
    db: Session,
    patient_id: int,
    name=None,
    age=None,
    phone=None,
    doctor_id=None
):
    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"

    if doctor_id is not None:
        doctor = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()

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

    db.commit()
    db.refresh(patient)

    return patient, None


def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)

    if not patient:
        return None

    db.delete(patient)
    db.commit()

    return patient
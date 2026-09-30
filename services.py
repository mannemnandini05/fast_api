from datetime import datetime,date,timedelta
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Appointment, Doctor, Patient,Billing


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

def create_billing(
    db: Session,
    patient_id,
    doctor_id,
    appointment_id,
    consultation_fee,
    additional_charges,
    payment_status,
    payment_mode,
):
    try:
        # Check patient
        patient = (
            db.query(Patient)
            .filter(Patient.id == patient_id)
            .first()
        )

        if not patient:
            return None, "Patient not found"

        # Check doctor
        doctor = (
            db.query(Doctor)
            .filter(Doctor.id == doctor_id)
            .first()
        )

        if not doctor:
            return None, "Doctor not found"

        if not doctor.is_active:
            return None, "Doctor is inactive"

        appointment = None

        # Check appointment if provided
        if appointment_id is not None:
            appointment = (
                db.query(Appointment)
                .filter(Appointment.id == appointment_id)
                .first()
            )

            if not appointment:
                return None, "Appointment not found"

            if appointment.doctor_id != doctor_id:
                return None, "Appointment does not belong to this doctor"

            if appointment.patient_id != patient_id:
                return None, "Appointment does not belong to this patient"

            if appointment.status == "cancelled":
                return None, "Cannot create billing for cancelled appointment"

            # Prevent duplicate billing
            existing_billing = (
                db.query(Billing)
                .filter(Billing.appointment_id == appointment_id)
                .first()
            )

            if existing_billing:
                return None, "Billing already exists for this appointment"

        # Auto-calculate total
        total_amount = consultation_fee + additional_charges

        billing = Billing(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            consultation_fee=consultation_fee,
            additional_charges=additional_charges,
            total_amount=total_amount,
            payment_status=payment_status,
            payment_mode=payment_mode,
            is_active=True,
        )

        db.add(billing)

        # Update appointment as part of the SAME transaction
        if appointment is not None:
            appointment.status = "completed"

        db.commit()
        db.refresh(billing)

        return billing, None

    except Exception:
        db.rollback()
        raise


def get_billing(db, billing_id):
    return (
        db.query(Billing)
        .filter(
            Billing.id == billing_id,
            Billing.is_active == True,
        )
        .first()
    )


def get_patient_billings(db, patient_id):
    return (
        db.query(Billing)
        .filter(
            Billing.patient_id == patient_id,
            Billing.is_active == True,
        )
        .order_by(Billing.created_at.desc())
        .all()
    )


def get_doctor_billings(db, doctor_id):
    return (
        db.query(Billing)
        .filter(
            Billing.doctor_id == doctor_id,
            Billing.is_active == True,
        )
        .order_by(Billing.created_at.desc())
        .all()
    )


def update_billing(
    db,
    billing_id,
    patient_id,
    doctor_id,
    appointment_id,
    consultation_fee,
    additional_charges,
    payment_status,
    payment_mode,
):
    billing = get_billing(db, billing_id)

    if not billing:
        return None, "Billing not found"

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        return None, "Patient not found"

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        return None, "Doctor not found"

    if not doctor.is_active:
        return None, "Doctor is inactive"

    if appointment_id is not None:
        appointment = (
            db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )

        if not appointment:
            return None, "Appointment not found"

        if appointment.doctor_id != doctor_id:
            return None, "Appointment does not belong to this doctor"

        if appointment.patient_id != patient_id:
            return None, "Appointment does not belong to this patient"

        if appointment.status == "cancelled":
            return None, "Cannot bill a cancelled appointment"

        duplicate = (
            db.query(Billing)
            .filter(
                Billing.appointment_id == appointment_id,
                Billing.id != billing_id,
            )
            .first()
        )

        if duplicate:
            return None, "Billing already exists for this appointment"

    billing.patient_id = patient_id
    billing.doctor_id = doctor_id
    billing.appointment_id = appointment_id
    billing.consultation_fee = consultation_fee
    billing.additional_charges = additional_charges
    billing.total_amount = consultation_fee + additional_charges
    billing.payment_status = payment_status
    billing.payment_mode = payment_mode

    db.commit()
    db.refresh(billing)

    return billing, None


def patch_billing(
    db,
    billing_id,
    patient_id=None,
    doctor_id=None,
    appointment_id=None,
    consultation_fee=None,
    additional_charges=None,
    payment_status=None,
    payment_mode=None,
):
    billing = get_billing(db, billing_id)

    if not billing:
        return None, "Billing not found"

    new_patient_id = (
        patient_id if patient_id is not None else billing.patient_id
    )

    new_doctor_id = (
        doctor_id if doctor_id is not None else billing.doctor_id
    )

    new_appointment_id = (
        appointment_id
        if appointment_id is not None
        else billing.appointment_id
    )

    new_consultation_fee = (
        consultation_fee
        if consultation_fee is not None
        else billing.consultation_fee
    )

    new_additional_charges = (
        additional_charges
        if additional_charges is not None
        else billing.additional_charges
    )

    new_payment_status = (
        payment_status
        if payment_status is not None
        else billing.payment_status
    )

    new_payment_mode = (
        payment_mode
        if payment_mode is not None
        else billing.payment_mode
    )

    updated_billing, error = update_billing(
        db,
        billing_id,
        new_patient_id,
        new_doctor_id,
        new_appointment_id,
        new_consultation_fee,
        new_additional_charges,
        new_payment_status,
        new_payment_mode,
    )

    return updated_billing, error


def delete_billing(db, billing_id):
    billing = get_billing(db, billing_id)

    if not billing:
        return None

    billing.is_active = False

    db.commit()
    db.refresh(billing)

    return billing
def get_billings(
    db,
    payment_status=None,
    doctor_id=None,
    patient_id=None,
    from_date=None,
    to_date=None,
    page=1,
    limit=10,
):
    query = db.query(Billing).filter(Billing.is_active == True)

    if payment_status:
        query = query.filter(
            Billing.payment_status == payment_status
        )

    if doctor_id:
        query = query.filter(
            Billing.doctor_id == doctor_id
        )

    if patient_id:
        query = query.filter(
            Billing.patient_id == patient_id
        )

    if from_date:
        query = query.filter(
            Billing.created_at >= from_date
        )

    if to_date:
        query = query.filter(
            Billing.created_at <= to_date
        )

    total = query.count()

    billings = (
        query
        .order_by(Billing.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return total, billings
def get_revenue_report(
    db: Session,
    doctor_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
):
    query = db.query(
        Billing.doctor_id,
        func.sum(Billing.total_amount).label("total_revenue"),
    ).filter(
        Billing.is_active == True,
        Billing.payment_status == "paid",
    )

    if doctor_id is not None:
        query = query.filter(Billing.doctor_id == doctor_id)

    if from_date is not None:
        query = query.filter(
            Billing.created_at >= datetime.combine(from_date, datetime.min.time())
        )

    if to_date is not None:
        query = query.filter(
            Billing.created_at < datetime.combine(
                to_date + timedelta(days=1),
                datetime.min.time(),
            )
        )

    return query.group_by(Billing.doctor_id).all()
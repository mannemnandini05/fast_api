from datetime import datetime
from typing import Optional, Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user, require_admin
from database import get_db
from models import Billing,Doctor
from schemas import (
    BillingCreate,
    BillingUpdate,
    BillingPatch,
    BillingResponse,
    BillingPageResponse,
)
import services


router = APIRouter(prefix="/billings", tags=["Billings"])


@router.post("/", response_model=BillingResponse, status_code=201)
def create_billing(
    billing: BillingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    new_billing, error = services.create_billing(
        db,
        billing.patient_id,
        billing.doctor_id,
        billing.appointment_id,
        billing.consultation_fee,
        billing.additional_charges,
        billing.payment_status,
        billing.payment_mode,
    )

    if error == "Patient not found":
        raise HTTPException(status_code=404, detail=error)

    if error == "Doctor not found":
        raise HTTPException(status_code=404, detail=error)

    if error == "Appointment not found":
        raise HTTPException(status_code=404, detail=error)

    if error == "Doctor is inactive":
        raise HTTPException(status_code=400, detail=error)

    if error == "Cannot create billing for a cancelled appointment":
        raise HTTPException(status_code=400, detail=error)

    if error == "Appointment does not belong to this doctor":
        raise HTTPException(status_code=400, detail=error)

    if error == "Appointment does not belong to this patient":
        raise HTTPException(status_code=400, detail=error)

    if error == "Billing already exists for this appointment":
        raise HTTPException(status_code=400, detail=error)

    return new_billing

@router.get("/", response_model=BillingPageResponse)
def get_billings(
    payment_status: Optional[
        Literal["pending", "paid", "cancelled"]
    ] = None,
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be greater than 0",
        )

    if from_date and to_date and from_date > to_date:
        raise HTTPException(
            status_code=400,
            detail="from_date cannot be greater than to_date",
        )

    if current_user.get("role") == "admin":
        total, billings = services.get_billings(
            db,
            payment_status,
            doctor_id,
            patient_id,
            from_date,
            to_date,
            page,
            limit,
        )

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": billings,
        }

    if current_user.get("role") == "doctor":
        doctor = (
            db.query(Doctor)
            .filter(
                Doctor.email == current_user.get("email")
            )
            .first()
        )

        if not doctor:
            raise HTTPException(
                status_code=403,
                detail="Doctor profile not found",
            )

        total, billings = services.get_billings(
            db,
            payment_status,
            doctor.id,
            patient_id,
            from_date,
            to_date,
            page,
            limit,
        )

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": billings,
        }

    raise HTTPException(
        status_code=403,
        detail="Access denied",
    )


@router.get("/{billing_id}", response_model=BillingResponse)
def get_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    billing = services.get_billing(db, billing_id)

    if not billing:
        raise HTTPException(
            status_code=404,
            detail="Billing not found",
        )

    if current_user.get("role") == "admin":
        return billing

    if current_user.get("role") == "doctor":
        doctor = services.get_doctor(db, billing.doctor_id)

        if not doctor or current_user.get("email") != doctor.email:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view billing for their patients",
            )

        return billing

    raise HTTPException(
        status_code=403,
        detail="Access denied",
    )




@router.get(
    "/patients/{patient_id}",
    response_model=list[BillingResponse],
)
def get_patient_billings(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user.get("role") == "admin":
        return services.get_patient_billings(db, patient_id)

    if current_user.get("role") == "doctor":
        patient = services.get_patient(db, patient_id)

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found",
            )

        doctor = services.get_doctor(db, patient.doctor_id)

        if not doctor or current_user.get("email") != doctor.email:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view billing for their patients",
            )

        return services.get_patient_billings(db, patient_id)

    raise HTTPException(
        status_code=403,
        detail="Access denied",
    )




@router.get(
    "/doctors/{doctor_id}",
    response_model=list[BillingResponse],
)
def get_doctor_billings(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    doctor = services.get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    if current_user.get("role") == "admin":
        return services.get_doctor_billings(db, doctor_id)

    if current_user.get("role") == "doctor":
        if current_user.get("email") != doctor.email:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view their own patient billings",
            )

        return services.get_doctor_billings(db, doctor_id)

    raise HTTPException(
        status_code=403,
        detail="Access denied",
    )




@router.put("/{billing_id}", response_model=BillingResponse)
def update_billing(
    billing_id: int,
    billing: BillingUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    updated_billing, error = services.update_billing(
        db,
        billing_id,
        billing.patient_id,
        billing.doctor_id,
        billing.appointment_id,
        billing.consultation_fee,
        billing.additional_charges,
        billing.payment_status,
        billing.payment_mode,
    )

    if error == "Billing not found":
        raise HTTPException(status_code=404, detail=error)

    if error in [
        "Patient not found",
        "Doctor not found",
        "Appointment not found",
    ]:
        raise HTTPException(status_code=404, detail=error)

    if error in [
        "Doctor is inactive",
        "Cannot bill a cancelled appointment",
        "Appointment does not belong to this doctor",
        "Appointment does not belong to this patient",
        "Billing already exists for this appointment",
    ]:
        raise HTTPException(status_code=400, detail=error)

    return updated_billing




@router.patch("/{billing_id}", response_model=BillingResponse)
def patch_billing(
    billing_id: int,
    billing: BillingPatch,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    updated_billing, error = services.patch_billing(
        db,
        billing_id,
        billing.patient_id,
        billing.doctor_id,
        billing.appointment_id,
        billing.consultation_fee,
        billing.additional_charges,
        billing.payment_status,
        billing.payment_mode,
    )

    if error == "Billing not found":
        raise HTTPException(status_code=404, detail=error)

    if error in [
        "Patient not found",
        "Doctor not found",
        "Appointment not found",
    ]:
        raise HTTPException(status_code=404, detail=error)

    if error in [
        "Doctor is inactive",
        "Cannot bill a cancelled appointment",
        "Appointment does not belong to this doctor",
        "Appointment does not belong to this patient",
        "Billing already exists for this appointment",
    ]:
        raise HTTPException(status_code=400, detail=error)

    return updated_billing




@router.delete("/{billing_id}")
def delete_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    billing = services.delete_billing(db, billing_id)

    if not billing:
        raise HTTPException(
            status_code=404,
            detail="Billing not found",
        )

    return {
        "message": "Billing deactivated successfully",
    }
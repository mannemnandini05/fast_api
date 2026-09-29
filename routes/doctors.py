from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user, require_admin
from database import get_db
import services

from schemas import (
    DoctorCreate,
    DoctorResponse,
    DoctorPatch,
    DoctorUpdate,
    PatientResponse,
    DoctorPageResponse,
)


router = APIRouter(prefix="/doctors", tags=["Doctors"])




@router.post("/", response_model=DoctorResponse, status_code=201)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    new_doctor = services.create_doctor(
        db,
        doctor.name,
        doctor.specialization,
        doctor.email,
        int(current_user["sub"]),
    )

    if new_doctor is None:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists",
        )

    return new_doctor




@router.get("/", response_model=DoctorPageResponse)
def get_doctors(
    specialization: str | None = None,
    is_active: bool | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be greater than 0",
        )

    total, doctors = services.get_doctors(
        db,
        specialization,
        is_active,
        page,
        limit,
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": doctors,
    }




@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    doctor = services.get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return doctor



@router.get(
    "/{doctor_id}/patients",
    response_model=list[PatientResponse],
)
def get_doctor_patients(
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

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Doctor is inactive",
        )

    user_role = current_user.get("role")

    if user_role == "admin":
        return services.get_doctor_patients(
            db,
            doctor_id,
        )

    if user_role == "doctor":
        if current_user.get("email") != doctor.email:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view their assigned patients",
            )

        return services.get_doctor_patients(
            db,
            doctor_id,
        )

    raise HTTPException(
        status_code=403,
        detail="Access denied",
    )




@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    updated_doctor, error = services.update_doctor(
        db,
        doctor_id,
        doctor.name,
        doctor.specialization,
        doctor.email,
        int(current_user["sub"]),
    )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor email already exists":
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return updated_doctor




@router.patch("/{doctor_id}", response_model=DoctorResponse)
def patch_doctor(
    doctor_id: int,
    doctor: DoctorPatch,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    updated_doctor, error = services.patch_doctor(
        db,
        doctor_id,
        doctor.name,
        doctor.specialization,
        doctor.email,
        int(current_user["sub"]),
    )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor email already exists":
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return updated_doctor


# =========================================================
# DELETE / DEACTIVATE DOCTOR - ADMIN ONLY
# =========================================================

@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    doctor = services.delete_doctor(
        db,
        doctor_id,
        int(current_user["sub"]),
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return {
        "message": "Doctor deactivated successfully",
    }

@router.post(
    "/{doctor_id}/patients/{patient_id}",
    response_model=PatientResponse,
)
def assign_patient(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    patient, error = services.assign_patient_to_doctor(
        db,
        doctor_id,
        patient_id,
        int(current_user["sub"]),
    )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Patient not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor is inactive":
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return patient



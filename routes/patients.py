from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from auth import require_admin
from database import get_db
import services

from schemas import (
    PatientCreate,
    PatientResponse,
    PatientPatch,
    PatientUpdate,
    PatientPageResponse,
)


router = APIRouter(prefix="/patients", tags=["Patients"])
@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    patient_data, error = services.create_patient(
        db,
        patient.name,
        patient.age,
        patient.phone,
        patient.doctor_id,
        int(current_user["sub"]),
    )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor is inactive":
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return patient_data




@router.get("/", response_model=PatientPageResponse)
def get_patients(
    age_gt:Optional[int]  = None,
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

    total, patients = services.get_patients(
        db,
        age_gt,
        page,
        limit,
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": patients,
    }




@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    patient = services.get_patient(
        db,
        patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient



@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    updated_patient, error = services.update_patient(
        db,
        patient_id,
        patient.name,
        patient.age,
        patient.phone,
        patient.doctor_id,
        int(current_user["sub"]),
    )

    if error == "Patient not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor is inactive":
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return updated_patient




@router.patch("/{patient_id}", response_model=PatientResponse)
def patch_patient(
    patient_id: int,
    patient: PatientPatch,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    updated_patient, error = services.patch_patient(
        db,
        patient_id,
        patient.name,
        patient.age,
        patient.phone,
        patient.doctor_id,
        int(current_user["sub"]),
    )

    if error == "Patient not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Doctor is inactive":
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return updated_patient




@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    patient = services.delete_patient(
        db,
        patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return {
        "message": "Patient deleted successfully",
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import services


from database import get_db
from models import Doctor, Patient
from schemas import PatientCreate, PatientResponse,PatientPatch,PatientUpdate,PatientPageResponse

router = APIRouter(prefix="/patients", tags=["Patients"])
@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    new_patient, error = services.create_patient(
        db,
        patient.name,
        patient.age,
        patient.phone,
        patient.doctor_id
    )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Doctor is inactive":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return new_patient

@router.get("/", response_model=PatientPageResponse)
def get_patients(
    age_gt: int | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be greater than 0"
        )

    total, patients = services.get_patients(
        db,
        age_gt,
        page,
        limit
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": patients
    }
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = services.get_patient(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient
@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient, error = services.update_patient(
        db,
        patient_id,
        patient_data.name,
        patient_data.age,
        patient_data.phone,
        patient_data.doctor_id
    )

    if error == "Patient not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Doctor is inactive":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return patient

@router.patch("/{patient_id}", response_model=PatientResponse)
def patch_patient(
    patient_id: int,
    patient_data: PatientPatch,
    db: Session = Depends(get_db)
):
    patient, error = services.patch_patient(
        db,
        patient_id,
        patient_data.name,
        patient_data.age,
        patient_data.phone,
        patient_data.doctor_id
    )

    if error == "Patient not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Doctor is inactive":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return patient

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = services.delete_patient(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {
        "message": "Patient deleted successfully"
    }
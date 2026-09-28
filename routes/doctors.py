from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Doctor
import services
from schemas import(

DoctorCreate, DoctorResponse,DoctorPatch,DoctorUpdate,PatientResponse,DoctorPageResponse)

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorResponse, status_code=201)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    new_doctor = services.create_doctor(
        db,
        doctor.name,
        doctor.specialization,
        doctor.email
    )

    if new_doctor is None:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    return new_doctor
@router.get("/", response_model=DoctorPageResponse)
def get_doctors(
    specialization: str | None = None,
    is_active: bool | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be greater than 0"
        )

    total, doctors = services.get_doctors(
        db,
        specialization,
        is_active,
        page,
        limit
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": doctors
    }

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = services.get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.get("/{doctor_id}/patients", response_model=list[PatientResponse])
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = services.get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Doctor is inactive"
        )

    return services.get_doctor_patients(
        db,
        doctor_id
    )
@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorUpdate,
    db: Session = Depends(get_db)
):
    doctor, error = services.update_doctor(
        db,
        doctor_id,
        doctor_data.name,
        doctor_data.specialization,
        doctor_data.email
    )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Doctor email already exists":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return doctor
@router.patch("/{doctor_id}", response_model=DoctorResponse)
def patch_doctor(
    doctor_id: int,
    doctor_data: DoctorPatch,
    db: Session = Depends(get_db)
):
    doctor, error = services.patch_doctor(
        db,
        doctor_id,
        doctor_data.name,
        doctor_data.specialization,
        doctor_data.email
    )

    if error == "Doctor not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Doctor email already exists":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = services.delete_doctor(
        db,
        doctor_id
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return {
        "message": "Doctor deactivated successfully"
    }


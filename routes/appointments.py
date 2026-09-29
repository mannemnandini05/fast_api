from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import services
from auth import get_current_user, require_admin
from database import get_db
from schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse


router = APIRouter(tags=["Appointments"])


# Create Appointment - Admin only
@router.post("/appointments", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    result, error = services.create_appointment(
    db,
    appointment.doctor_id,
    appointment.patient_id,
    appointment.appointment_date,
    appointment.status,
    int(current_user["sub"])
)
    if error:
        raise HTTPException(status_code=400, detail=error)

    return result


# List All Appointments - Admin only
@router.get("/appointments", response_model=list[AppointmentResponse])
def get_appointments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    return services.get_appointments(db)


# Get Appointment by ID - Admin only
@router.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    appointment = services.get_appointment(db, appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


# Update Appointment - Admin only
@router.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    result, error = services.update_appointment(
    db,
    appointment_id,
    appointment.doctor_id,
    appointment.patient_id,
    appointment.appointment_date,
    appointment.status,
    int(current_user["sub"])
)
    if error == "Appointment not found":
        raise HTTPException(status_code=404, detail=error)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return result


# Delete Appointment - Admin only
@router.delete("/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    result = services.delete_appointment(db, appointment_id)

    if not result:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {"message": "Appointment deleted successfully"}


# Get Doctor's Appointments
# Required endpoint:
# GET /api/v1/doctors/{doctor_id}/appointments
@router.get(
    "/doctors/{doctor_id}/appointments",
    response_model=list[AppointmentResponse]
)
def get_doctor_appointments(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    doctor = services.get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if current_user.get("role") == "doctor":
        if current_user.get("email") != doctor.email:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own appointments"
            )

    return services.get_doctor_appointments(db, doctor_id)


# Get Patient's Appointments
# Required endpoint:
# GET /api/v1/patients/{patient_id}/appointments
@router.get(
    "/patients/{patient_id}/appointments",
    response_model=list[AppointmentResponse]
)
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    patient = services.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return services.get_patient_appointments(db, patient_id)
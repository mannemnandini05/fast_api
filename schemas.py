from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field




class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Dr. Ravi Kumar",
                "specialization": "Cardiology",
                "email": "ravi.kumar@example.com"
            }
        }
    )


class DoctorUpdate(BaseModel):
    name: str
    specialization: str
    email: EmailStr


class DoctorPatch(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[EmailStr] = None


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool

    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)



class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10,15}$")
    doctor_id: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "age": 30,
                "phone": "9876543210",
                "doctor_id": 1
            }
        }
    )


class PatientUpdate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10,15}$")
    doctor_id: Optional[int] = None


class PatientPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^\d{10,15}$"
    )
    doctor_id: Optional[int] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: Optional[int] = None

    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: Literal["scheduled", "completed", "cancelled"] = "scheduled"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "doctor_id": 1,
                "patient_id": 1,
                "appointment_date": "2026-10-15T10:30:00",
                "status": "scheduled"
            }
        }
    )

class AppointmentUpdate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: Literal["scheduled", "completed", "cancelled"]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "doctor_id": 1,
                "patient_id": 1,
                "appointment_date": "2026-10-15T10:30:00",
                "status": "completed"
            }
        }
    )


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: Literal[
        "scheduled",
        "completed",
        "cancelled"
    ]

    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)




class DoctorPageResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[DoctorResponse]


class PatientPageResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[PatientResponse]




class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Literal["admin", "doctor"] = "doctor"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "Admin@123",
                "role": "admin"
            }
        }
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "Admin@123"
            }
        }
    )



class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
class BillingCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    consultation_fee: int = Field(ge=0)
    additional_charges: int = Field(ge=0, default=0)
    payment_status: Literal["pending", "paid", "cancelled"] = "pending"
    payment_mode: Literal["cash", "card", "upi"]


class BillingUpdate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    consultation_fee: int = Field(ge=0)
    additional_charges: int = Field(ge=0)
    payment_status: Literal["pending", "paid", "cancelled"]
    payment_mode: Literal["cash", "card", "upi"]


class BillingPatch(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_id: Optional[int] = None
    consultation_fee: Optional[int] = Field(default=None, ge=0)
    additional_charges: Optional[int] = Field(default=None, ge=0)
    payment_status: Optional[Literal["pending", "paid", "cancelled"]] = None
    payment_mode: Optional[Literal["cash", "card", "upi"]] = None


class BillingResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    consultation_fee: int
    additional_charges: int
    total_amount: int
    payment_status: Literal["pending", "paid", "cancelled"]
    payment_mode: Literal["cash", "card", "upi"]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
class BillingPageResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[BillingResponse]
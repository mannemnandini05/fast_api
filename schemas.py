from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr

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

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10}$")
    doctor_id: Optional[int] = None

class PatientUpdate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10}$")
    doctor_id: Optional[int] = None


class PatientPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = Field(default=None, pattern=r"^\d{10}$")
    doctor_id: Optional[int] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: Optional[int]

    class Config:
        from_attributes = True
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
    role: str = "admin"


class UserLogin(BaseModel):
    email: EmailStr
    password: str

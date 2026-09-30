from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    patients = relationship("Patient", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    billings = relationship("Billing", back_populates="doctor")

    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_doctors",
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by],
        back_populates="updated_doctors",
    )


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(15), nullable=False)

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=True,
        index=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    doctor = relationship("Doctor", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    billings = relationship("Billing", back_populates="patient")

    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_patients",
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by],
        back_populates="updated_patients",
    )

    __table_args__ = (
        CheckConstraint("age > 0", name="check_patient_age_positive"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="admin", nullable=False)

    created_doctors = relationship(
        "Doctor",
        foreign_keys="Doctor.created_by",
        back_populates="creator",
    )

    updated_doctors = relationship(
        "Doctor",
        foreign_keys="Doctor.updated_by",
        back_populates="updater",
    )

    created_patients = relationship(
        "Patient",
        foreign_keys="Patient.created_by",
        back_populates="creator",
    )

    updated_patients = relationship(
        "Patient",
        foreign_keys="Patient.updated_by",
        back_populates="updater",
    )

    created_appointments = relationship(
        "Appointment",
        foreign_keys="Appointment.created_by",
        back_populates="creator",
    )

    updated_appointments = relationship(
        "Appointment",
        foreign_keys="Appointment.updated_by",
        back_populates="updater",
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False,
        index=True,
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True,
    )

    appointment_date = Column(
        DateTime,
        nullable=False,
        index=True,
    )

    status = Column(
        String(20),
        nullable=False,
        default="scheduled",
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    billing = relationship("Billing", back_populates="appointment", uselist=False)    
    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_appointments",
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by],
        back_populates="updated_appointments",
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled')",
            name="check_appointment_status",
        ),
        UniqueConstraint(
            "doctor_id",
            "appointment_date",
            name="unique_doctor_appointment_time",
        ),
        Index(
            "ix_appointments_doctor_date",
            "doctor_id",
            "appointment_date",
        ),
    )
class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False,
        index=True
    )

    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
        nullable=True,
        unique=True,
        index=True
    )

    consultation_fee = Column(Integer, nullable=False)
    additional_charges = Column(Integer, nullable=False, default=0)
    total_amount = Column(Integer, nullable=False)

    payment_status = Column(
        String(20),
        nullable=False,
        default="pending"
    )

    payment_mode = Column(
        String(20),
        nullable=False
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    patient = relationship("Patient", back_populates="billings")
    doctor = relationship("Doctor", back_populates="billings")
    appointment = relationship("Appointment", back_populates="billing")

    __table_args__ = (
        CheckConstraint(
            "consultation_fee >= 0",
            name="check_consultation_fee_positive"
        ),
        CheckConstraint(
            "additional_charges >= 0",
            name="check_additional_charges_positive"
        ),
        CheckConstraint(
            "total_amount >= 0",
            name="check_total_amount_positive"
        ),
        CheckConstraint(
            "payment_status IN ('pending', 'paid', 'cancelled')",
            name="check_payment_status"
        ),
        CheckConstraint(
            "payment_mode IN ('cash', 'card', 'upi')",
            name="check_payment_mode"
        ),
    )
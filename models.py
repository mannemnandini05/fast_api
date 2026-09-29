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
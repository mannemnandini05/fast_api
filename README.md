# Doctor Patient Management System

A backend application built using FastAPI for managing doctors, patients, appointments, authentication, authorization, and database operations.

## Tech Stack

- Python 3.9+
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn
- Pytest
- Pytest-Cov

## Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Protected APIs
- Role-based authorization

### Roles

#### Admin

- Manage doctors
- Manage patients
- Manage appointments
- Assign patients to doctors
- View all records

#### Doctor

- View assigned patients
- View own appointments
- Cannot delete doctors
- Cannot delete patients

## Doctor APIs

- `POST /api/v1/doctors`
- `GET /api/v1/doctors`
- `GET /api/v1/doctors/{doctor_id}`
- `PUT /api/v1/doctors/{doctor_id}`
- `PATCH /api/v1/doctors/{doctor_id}`
- `DELETE /api/v1/doctors/{doctor_id}`

### Doctor-Patient Assignment

- `POST /api/v1/doctors/{doctor_id}/patients/{patient_id}`
- `GET /api/v1/doctors/{doctor_id}/patients`

## Patient APIs

- `POST /api/v1/patients`
- `GET /api/v1/patients`
- `GET /api/v1/patients/{patient_id}`
- `PUT /api/v1/patients/{patient_id}`
- `PATCH /api/v1/patients/{patient_id}`
- `DELETE /api/v1/patients/{patient_id}`

## Appointment APIs

- `POST /api/v1/appointments`
- `GET /api/v1/appointments`
- `GET /api/v1/appointments/{appointment_id}`
- `PUT /api/v1/appointments/{appointment_id}`
- `DELETE /api/v1/appointments/{appointment_id}`
- `GET /api/v1/doctors/{doctor_id}/appointments`
- `GET /api/v1/patients/{patient_id}/appointments`

## Appointment Rules

- Doctor must exist.
- Patient must exist.
- Doctor must be active.
- Patient must be assigned to the doctor.
- Appointment status can be:
  - scheduled
  - completed
  - cancelled
- A doctor cannot have two appointments at the same date and time.

## Validation

- Email validation
- Unique doctor email
- Patient age must be greater than 0
- Phone number must contain 10–15 digits
- Appointment status validation

## Audit Fields

The application tracks:

- `created_at`
- `updated_at`
- `created_by`
- `updated_by`

JWT user information is used for tracking the user who creates or updates records.

## Error Handling

The application includes:

- Global HTTP exception handling
- Validation error handling
- Database constraint error handling
- SQLAlchemy database error handling
- Unexpected error handling
- Uniform error responses

## Rate Limiting

A basic in-memory rate limiter is implemented to restrict excessive requests from the same client.

## API Documentation

Swagger UI is available at:

`http://127.0.0.1:8000/docs`

ReDoc is available at:

`http://127.0.0.1:8000/redoc`

## Running the Application

Create and activate a virtual environment:

```bash
python -m venv venv
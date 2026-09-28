# Doctor Patient Management System

A FastAPI-based backend application for managing doctors and patients with JWT authentication, role-based authorization, and database persistence.

## Technologies Used

- Python 3.9+
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn

## Features

### Authentication
- User registration
- User login
- JWT-based authentication
- Protected APIs
- Role-based authorization

### Doctor Management
- Create doctor
- View all doctors
- View doctor by ID
- Update doctor
- Delete doctor

### Patient Management
- Create patient
- View all patients
- View patient by ID
- Update patient
- Delete patient

### Doctor-Patient Assignment
- Assign a patient to a doctor
- View patients assigned to a doctor
- Doctors can view their assigned patients

### Validation
- Unique doctor email
- Valid email format
- Patient age must be greater than 0
- Patient phone number validation

## Project Structure

```text
fastapi/
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── doctors.py
│   └── patients.py
│
├── auth.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── services.py
├── requirements.txt
├── .gitignore
└── README.md
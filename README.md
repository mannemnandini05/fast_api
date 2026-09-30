# Doctor Patient Management API

A backend REST API built with FastAPI for managing doctors, patients, appointments, billing, authentication, authorization, and reports.

## Technologies Used

- Python 3.9+
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- pwdlib Password Hashing
- Uvicorn
- Pytest
- Pytest-Cov
- HTTPX
- Swagger / OpenAPI

## Project Features

- User registration and login
- JWT-based authentication
- Role-based authorization
- Admin and Doctor roles
- Doctor management
- Patient management
- Doctor-patient assignment
- Appointment management
- Billing management
- Revenue reporting
- Request validation
- Database constraints
- Global exception handling
- Custom error responses
- Basic rate limiting
- Response-time measurement
- Audit fields
- Automated testing
- Swagger API documentation

## Authentication

The application uses JWT-based authentication.

### Register

```text
POST /api/v1/auth/register
Login
POST /api/v1/auth/login
The login response provides an access token.
Use the token in Swagger by clicking:
Authorize
and entering:
Bearer <access_token>
Protected APIs require a valid JWT token.
User Roles
The application supports two roles:
Admin
Admin users can manage:
Doctors
Patients
Appointments
Billing
Reports
Doctor
Doctors can access resources according to their assigned records and role permissions.
Doctors cannot perform admin-only operations such as deleting doctors or patients.
Unauthorized requests return:
401 Unauthorized
Requests that are authenticated but do not have sufficient permissions return:
403 Forbidden
Doctor Management
Doctor APIs support:
Create doctor
Get doctors
Get doctor by ID
Update doctor
Patch doctor
Delete/deactivate doctor
Assign patients
View assigned patients
View doctor appointments
Doctor information includes:
Name
Specialization
Email
Active status
Created date
Updated date
Created by
Updated by
Doctor email addresses are unique.
Patient Management
Patient APIs support:
Create patient
Get patients
Get patient by ID
Update patient
Patch patient
Delete patient
Assign patient to a doctor
Patient information includes:
Name
Age
Phone number
Doctor ID
Created date
Updated date
Created by
Updated by
Validation rules include:
Age must be greater than 0
Phone number must contain 10–15 digits
Doctor-Patient Assignment
Patients can be assigned to doctors.
The system validates:
Doctor exists
Patient exists
Doctor is active
The assigned doctor can access their assigned patients according to authorization rules.
Appointment Management
Appointment APIs support:
Create appointment
Get appointments
Get appointment by ID
Update appointment
Delete appointment
Get doctor appointments
Get patient appointments
Appointment fields include:
Doctor ID
Patient ID
Appointment date
Status
Supported appointment statuses:
scheduled
completed
cancelled
The system validates:
Doctor exists
Patient exists
Doctor is active
Patient is assigned to the doctor
The same doctor cannot have two appointments at the same date/time
Billing Management
Billing APIs support:
Create billing
Get billings
Get billing by ID
Update billing
Patch billing
Delete billing
Get patient billings
Get doctor billings
Billing fields include:
Patient ID
Doctor ID
Appointment ID
Consultation fee
Additional charges
Total amount
Payment status
Payment mode
Active status
Created date
Updated date
Payment statuses:
pending
paid
cancelled
Payment modes:
cash
card
upi
The billing total is calculated from:
Total Amount = Consultation Fee + Additional Charges
Billing validation also checks that the related patient and doctor exist and that the doctor is active.
Reports
The application provides revenue reporting.
Revenue Report
GET /api/v1/reports/revenue
Optional filters can be used for:
Doctor
From date
To date
The report returns the requested revenue information based on available billing records.
Database
The application uses SQLite.
Database file:
doctor_patient.db
The database is automatically created when the application starts.
SQLite foreign-key support is enabled.
Database constraints include:
Unique doctor email
Unique user email
Foreign keys
Positive patient age
Valid appointment status
Unique doctor appointment time
Valid billing payment status
Valid billing payment mode
Non-negative billing amounts
Audit Fields
The application tracks:
created_at
updated_at
created_by
updated_by
JWT user information is used to identify the user responsible for creating or updating records.
Timestamps are automatically maintained by SQLAlchemy.
Error Handling
The application provides global exception handling for:
Validation errors
Database constraint errors
SQLAlchemy errors
Unexpected server errors
HTTP errors
Errors use a consistent response format.
Example:
{
  "success": false,
  "error": "HTTP Error",
  "message": "Not authenticated"
}
Validation errors provide additional details about invalid request data.
Rate Limiting
The application includes basic in-memory rate limiting.
The default limit is:
60 requests per 60 seconds per client
When the limit is exceeded, the API returns:
429 Too Many Requests
Response Time
API responses include an X-Response-Time response header.
Example:
X-Response-Time: 0.0124s
This can be used to measure API response time.
API Documentation
Swagger UI is available at:
http://127.0.0.1:8000/docs
OpenAPI JSON:
http://127.0.0.1:8000/openapi.json
ReDoc:
http://127.0.0.1:8000/redoc
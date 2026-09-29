from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database import Base, engine
from fastapi.responses import JSONResponse
from fastapi import Request,HTTPException
import models
import time
from collections import defaultdict
from routes.doctors import router as doctor_router
from routes.patients import router as patient_router
from routes.auth import router as auth_router
from routes.appointments import router as appointment_router


app = FastAPI(
    title="Doctor Patient Management API",
    description="Backend API for managing doctors, patients, authentication, and appointments.",
    version="2.0.0",
)
rate_limit_data = defaultdict(list)

RATE_LIMIT = 60
RATE_LIMIT_WINDOW = 60


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()

    # Skip documentation endpoints
    if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)

    request_times = rate_limit_data[client_ip]

    # Remove requests older than 60 seconds
    request_times[:] = [
        request_time
        for request_time in request_times
        if current_time - request_time < RATE_LIMIT_WINDOW
    ]

    if len(request_times) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
            },
        )

    request_times.append(current_time)

    return await call_next(request)
@app.middleware("http")
async def measure_response_time(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    response_time = time.perf_counter() - start_time

    response.headers["X-Response-Time"] = f"{response_time:.4f}s"

    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": "HTTP Error",
            "message": exc.detail
        }
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": "Database constraint error",
            "message": "The requested operation violates a database constraint."
        }
    )


@app.exception_handler(SQLAlchemyError)
async def database_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Database error",
            "message": "A database error occurred while processing the request."
        }
    )
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
        },
    )
# Create database tables
Base.metadata.create_all(bind=engine)


# Register routers
app.include_router(
    doctor_router,
    prefix="/api/v1",
)

app.include_router(
    patient_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    appointment_router,
    prefix="/api/v1",
)


@app.get("/")
def home():
    return {
        "message": "Doctor Patient Management API is running"
    }
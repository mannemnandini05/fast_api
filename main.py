from fastapi import FastAPI
from database import Base, engine
import models
from routes.doctors import router as doctor_router
from routes.patients import router as patient_router
app = FastAPI(
    title="Doctor Patient Management API"
)

Base.metadata.create_all(bind=engine)
app.include_router(
    doctor_router,
    prefix="/api/v1"
)

app.include_router(
    patient_router,
    prefix="/api/v1"
)



@app.get("/")
def home():
    return {"message": "Doctor Patient Management API is running"}
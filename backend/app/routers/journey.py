from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ai_modules.journey_optimizer import optimize_journey


router = APIRouter(
    prefix="/ai/journey",
    tags=["Multi-Appointment Journey Optimiser"]
)


class Appointment(BaseModel):
    centre_name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    appointment_time: str


class JourneyRequest(BaseModel):
    appointments: List[Appointment] = Field(..., min_length=1)
    starting_latitude: float = Field(..., ge=-90, le=90)
    starting_longitude: float = Field(..., ge=-180, le=180)
    average_speed_kmph: float = Field(default=30, gt=0)


@router.post("/optimize")
def optimize_patient_journey(request: JourneyRequest):

    try:
        appointments = [
            appointment.model_dump()
            for appointment in request.appointments
        ]

        result = optimize_journey(
            appointments=appointments,
            starting_latitude=request.starting_latitude,
            starting_longitude=request.starting_longitude,
            average_speed_kmph=request.average_speed_kmph
        )

        return {
            "success": True,
            "feature": "Multi-Appointment Journey Optimiser",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Journey optimization failed: {str(error)}"
        )


@router.get("/health")
def journey_health():
    return {
        "success": True,
        "feature": "Multi-Appointment Journey Optimiser",
        "status": "available"
    }
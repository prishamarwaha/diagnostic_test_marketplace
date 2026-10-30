from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai_modules.travel_planner import calculate_travel_plan


router = APIRouter(
    prefix="/ai/travel",
    tags=["AI Travel-Time and Departure Planner"]
)


class TravelPlanRequest(BaseModel):
    distance_km: float = Field(..., gt=0)
    appointment_time: str
    average_speed_kmph: float = Field(default=30, gt=0)
    buffer_minutes: int = Field(default=20, ge=0)
    preparation_minutes: int = Field(default=15, ge=0)


@router.post("/calculate")
def calculate_departure(request: TravelPlanRequest):

    try:
        result = calculate_travel_plan(
            distance_km=request.distance_km,
            appointment_time=request.appointment_time,
            average_speed_kmph=request.average_speed_kmph,
            buffer_minutes=request.buffer_minutes,
            preparation_minutes=request.preparation_minutes
        )

        return {
            "success": True,
            "feature": "AI Travel-Time and Departure Planner",
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
            detail=f"Travel planning failed: {str(error)}"
        )


@router.get("/health")
def travel_health():
    return {
        "success": True,
        "feature": "AI Travel-Time and Departure Planner",
        "status": "available"
    }
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ai_modules.capacity_balancer import balance_centre_capacity


router = APIRouter(
    prefix="/ai/capacity",
    tags=["Cross-Centre Capacity Balancing"]
)


class DiagnosticCentre(BaseModel):
    centre_name: str
    supported_tests: List[str]
    total_capacity: int = Field(..., ge=0)
    current_bookings: int = Field(..., ge=0)
    distance_km: float = Field(..., ge=0)


class CapacityRequest(BaseModel):
    centres: List[DiagnosticCentre] = Field(..., min_length=1)
    requested_test: str = Field(..., min_length=1)
    patient_count: int = Field(default=1, ge=1)


@router.post("/balance")
def balance_capacity(request: CapacityRequest):
    try:
        centres = [
            centre.model_dump()
            for centre in request.centres
        ]

        result = balance_centre_capacity(
            centres=centres,
            requested_test=request.requested_test,
            patient_count=request.patient_count
        )

        return {
            "success": True,
            "feature": "Cross-Centre Capacity Balancing",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Capacity balancing failed: {str(error)}"
        )


@router.get("/health")
def capacity_health():
    return {
        "success": True,
        "feature": "Cross-Centre Capacity Balancing",
        "status": "available"
    }
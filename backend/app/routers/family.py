from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ai_modules.family_coordinator import (
    coordinate_family_appointments
)

router = APIRouter(
    prefix="/ai/family",
    tags=["AI Family Appointment Coordinator"]
)


class FamilyMember(BaseModel):
    member_id: str
    member_name: str
    required_test: str
    preferred_centre: str
    available_times: List[str] = Field(..., min_length=1)


class FamilyCoordinationRequest(BaseModel):
    family_members: List[FamilyMember] = Field(..., min_length=1)


@router.post("/coordinate")
def coordinate_appointments(request: FamilyCoordinationRequest):
    try:
        family_members = [
            member.model_dump()
            for member in request.family_members
        ]

        result = coordinate_family_appointments(
            family_members=family_members
        )

        return {
            "success": True,
            "feature": "AI Family Appointment Coordinator",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Family coordination failed: {str(error)}"
        )


@router.get("/health")
def family_health():
    return {
        "success": True,
        "feature": "AI Family Appointment Coordinator",
        "status": "available"
    }
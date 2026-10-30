from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List


from app.ai_modules.staff_roster_optimizer import optimize_staff_roster


router = APIRouter(
    prefix="/ai/staff-roster",
    tags=["Staff Roster Optimisation"]
)


class StaffMember(BaseModel):
    staff_id: str
    name: str
    available: bool
    skills: List[str]
    working_hours: float = Field(..., ge=0)


class StaffRosterRequest(BaseModel):
    staff_members: List[StaffMember] = Field(..., min_length=1)
    required_staff: int = Field(..., ge=1)
    expected_patient_count: int = Field(..., ge=0)


@router.post("/optimize")
def optimize_roster(request: StaffRosterRequest):
    try:
        staff_members = [
            staff.model_dump()
            for staff in request.staff_members
        ]

        result = optimize_staff_roster(
            staff_members=staff_members,
            required_staff=request.required_staff,
            expected_patient_count=request.expected_patient_count
        )

        return {
            "success": True,
            "feature": "Staff Roster Optimisation",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Staff roster optimization failed: {str(error)}"
        )


@router.get("/health")
def staff_roster_health():
    return {
        "success": True,
        "feature": "Staff Roster Optimisation",
        "status": "available"
    }

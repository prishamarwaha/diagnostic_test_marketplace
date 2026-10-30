from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ai_modules.cancellation_recovery import (
    simulate_cancellation_recovery
)

router = APIRouter(
    prefix="/ai/cancellation",
    tags=["Cancellation Recovery Simulator"]
)


class CancelledSlot(BaseModel):
    slot_id: str
    centre_name: str
    test_name: str
    appointment_time: str


class WaitlistPatient(BaseModel):
    patient_id: str
    patient_name: str
    preferred_tests: List[str]
    available_times: List[str]
    priority: int = Field(..., ge=1, le=10)


class CancellationRequest(BaseModel):
    cancelled_slots: List[CancelledSlot] = Field(..., min_length=1)
    waitlist: List[WaitlistPatient] = Field(..., min_length=1)


@router.post("/simulate")
def recover_cancelled_slots(request: CancellationRequest):
    try:
        cancelled_slots = [
            slot.model_dump()
            for slot in request.cancelled_slots
        ]

        waitlist = [
            patient.model_dump()
            for patient in request.waitlist
        ]

        result = simulate_cancellation_recovery(
            cancelled_slots=cancelled_slots,
            waitlist=waitlist
        )

        return {
            "success": True,
            "feature": "Cancellation Recovery Simulator",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Cancellation recovery failed: {str(error)}"
        )


@router.get("/health")
def cancellation_health():
    return {
        "success": True,
        "feature": "Cancellation Recovery Simulator",
        "status": "available"
    }
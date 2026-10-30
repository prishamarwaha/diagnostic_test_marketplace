from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai_modules.equipment_maintenance import assess_equipment_risk


router = APIRouter(
    prefix="/ai/equipment-maintenance",
    tags=["Predictive Equipment Maintenance"]
)


class EquipmentMaintenanceRequest(BaseModel):
    equipment_name: str = Field(..., min_length=1)
    days_since_maintenance: int = Field(..., ge=0)
    usage_hours: float = Field(..., ge=0)
    average_daily_usage: float = Field(..., ge=0, le=24)
    fault_count: int = Field(..., ge=0)
    critical_fault_count: int = Field(..., ge=0)
    temperature_deviation: float = Field(..., ge=0)
    calibration_overdue: bool = False


@router.post("/assess")
def assess_maintenance(request: EquipmentMaintenanceRequest):
    try:
        result = assess_equipment_risk(
            equipment_name=request.equipment_name,
            days_since_maintenance=request.days_since_maintenance,
            usage_hours=request.usage_hours,
            average_daily_usage=request.average_daily_usage,
            fault_count=request.fault_count,
            critical_fault_count=request.critical_fault_count,
            temperature_deviation=request.temperature_deviation,
            calibration_overdue=request.calibration_overdue
        )

        return {
            "success": True,
            "feature": "Predictive Equipment Maintenance",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Equipment assessment failed: {str(error)}"
        )


@router.get("/health")
def equipment_maintenance_health():
    return {
        "success": True,
        "feature": "Predictive Equipment Maintenance",
        "status": "available"
    }
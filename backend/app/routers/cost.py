from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ai_modules.cost_estimator import estimate_diagnostic_cost


router = APIRouter(
    prefix="/ai/cost",
    tags=["Total Diagnostic Cost Estimator"]
)


class DiagnosticTest(BaseModel):
    test_name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)


class CostEstimateRequest(BaseModel):
    tests: List[DiagnosticTest] = Field(..., min_length=1)
    additional_charges: float = Field(default=0, ge=0)
    home_collection_charge: float = Field(default=0, ge=0)
    discount_percentage: float = Field(default=0, ge=0, le=100)
    tax_percentage: float = Field(default=0, ge=0, le=100)


@router.post("/estimate")
def calculate_diagnostic_cost(request: CostEstimateRequest):
    try:
        tests = [
            test.model_dump()
            for test in request.tests
        ]

        result = estimate_diagnostic_cost(
            tests=tests,
            additional_charges=request.additional_charges,
            home_collection_charge=request.home_collection_charge,
            discount_percentage=request.discount_percentage,
            tax_percentage=request.tax_percentage
        )

        return {
            "success": True,
            "feature": "Total Diagnostic Cost Estimator",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Cost estimation failed: {str(error)}"
        )


@router.get("/health")
def cost_health():
    return {
        "success": True,
        "feature": "Total Diagnostic Cost Estimator",
        "status": "available"
    }
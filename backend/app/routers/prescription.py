from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai_modules.prescription_extractor import process_prescription


router = APIRouter(
    prefix="/ai/prescription",
    tags=["AI Prescription Extraction"]
)


# Request body schema
class PrescriptionRequest(BaseModel):
    prescription_text: str = Field(
        ...,
        min_length=1,
        description="Text extracted or copied from the patient's prescription"
    )


# Main prescription extraction endpoint
@router.post("/extract")
def extract_prescription(request: PrescriptionRequest):

    try:
        # Remove unnecessary whitespace
        prescription_text = request.prescription_text.strip()

        # Validate input
        if not prescription_text:
            raise HTTPException(
                status_code=400,
                detail="Prescription text cannot be empty."
            )

        # Process prescription using the extraction module
        result = process_prescription(prescription_text)

        return {
            "success": True,
            "message": "Prescription processed successfully.",
            "data": {
                "extraction_method": result["extraction_method"],
                "total_tests_detected": result["total_tests_detected"],
                "extracted_tests": result["extracted_tests"],
                "unmatched_terms_for_review": result[
                    "unmatched_terms_for_review"
                ],
                "requires_clinical_review": result[
                    "requires_clinical_review"
                ]
            }
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prescription processing failed: {str(error)}"
        )


# Endpoint to check whether the prescription extraction module is available
@router.get("/health")
def prescription_health_check():
    return {
        "success": True,
        "feature": "AI Prescription-to-Test Extraction",
        "status": "available"
    }
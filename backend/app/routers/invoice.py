from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai_modules.invoice_extractor import extract_invoice_details


router = APIRouter(
    prefix="/ai/invoice",
    tags=["Automated Invoice and Tariff Extraction"]
)


class InvoiceRequest(BaseModel):
    invoice_text: str = Field(
        ...,
        min_length=1,
        description="Text copied or extracted from an invoice or tariff document"
    )


@router.post("/extract")
def extract_invoice(request: InvoiceRequest):
    try:
        result = extract_invoice_details(
            invoice_text=request.invoice_text
        )

        return {
            "success": True,
            "feature": "Automated Invoice and Tariff Extraction",
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Invoice extraction failed: {str(error)}"
        )


@router.get("/health")
def invoice_health():
    return {
        "success": True,
        "feature": "Automated Invoice and Tariff Extraction",
        "status": "available"
    }
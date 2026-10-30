from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ai_modules.document_checker import check_document_completeness


router = APIRouter(
    prefix="/ai/documents",
    tags=["Referral-Document Completeness Checker"]
)


class DocumentCheckRequest(BaseModel):
    required_documents: List[str] = Field(
        ...,
        min_length=1,
        description="Documents required by the diagnostic centre"
    )

    provided_documents: List[str] = Field(
        default_factory=list,
        description="Documents provided by the patient"
    )

    unreadable_documents: List[str] = Field(
        default_factory=list,
        description="Documents identified as unreadable"
    )


@router.post("/check-completeness")
def check_documents(request: DocumentCheckRequest):
    try:
        result = check_document_completeness(
            required_documents=request.required_documents,
            provided_documents=request.provided_documents,
            unreadable_documents=request.unreadable_documents
        )

        return {
            "success": True,
            "feature": "Referral-Document Completeness Checker",
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
            detail=f"Document check failed: {str(error)}"
        )


@router.get("/health")
def document_checker_health():
    return {
        "success": True,
        "feature": "Referral-Document Completeness Checker",
        "status": "available"
    }
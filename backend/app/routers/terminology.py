from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ai_modules.terminology_simplifier import (
    simplify_medical_term,
    simplify_multiple_terms
)


router = APIRouter(
    prefix="/ai/terminology",
    tags=["Medical Terminology Simplifier"]
)


class TerminologyRequest(BaseModel):
    term: str = Field(
        ...,
        min_length=1,
        description="Medical term or abbreviation to simplify"
    )


class MultipleTerminologyRequest(BaseModel):
    terms: List[str] = Field(
        ...,
        min_length=1,
        description="List of medical terms to simplify"
    )


@router.post("/simplify")
def simplify_term(request: TerminologyRequest):
    try:
        return {
            "success": True,
            "result": simplify_medical_term(request.term)
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/simplify-multiple")
def simplify_terms(request: MultipleTerminologyRequest):
    try:
        return {
            "success": True,
            "result": simplify_multiple_terms(request.terms)
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/health")
def terminology_health_check():
    return {
        "success": True,
        "feature": "Medical Terminology Simplifier",
        "status": "available"
    }
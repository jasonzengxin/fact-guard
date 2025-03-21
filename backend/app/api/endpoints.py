from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from app.services.analysis_service import AnalysisService

router = APIRouter()

class FactCheckRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class FactCheckResponse(BaseModel):
    claims: List[str]

class ClaimResponse(BaseModel):
    claims: List[str]

# Initialize AnalysisService
analysis_service = AnalysisService()

@router.post("/extract_claims", response_model=ClaimResponse)
async def extract_claims(request: FactCheckRequest):
    """
    Extract claims from text or URL content.
    
    Args:
        request (FactCheckRequest): Request containing text or URL
        
    Returns:
        ClaimResponse: List of extracted claims
        
    Raises:
        HTTPException: If neither text nor URL is provided
    """
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Either text or URL must be provided")
    
    try:
        # For now, we only handle text input
        # TODO: Add URL content extraction
        text = request.text or ""
        claims = await analysis_service.claim_extractor.extract_claims(text)
        
        return ClaimResponse(claims=claims)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting claims: {str(e)}")

@router.post("/check")
async def check_facts(request: FactCheckRequest):
    """
    Check facts from provided text or URL.
    """
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Either text or URL must be provided")
    
    # TODO: Implement actual fact checking logic
    # For now, return dummy data
    return {
        "is_fact": True,
        "confidence": 0.85,
        "explanation": "This is a test explanation",
        "sources": [],
        "discrepancies": []
    } 
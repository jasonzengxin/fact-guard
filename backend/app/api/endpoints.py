from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from ..models.schemas import FactCheckRequest, FactCheckResponse
from ..services.analysis_service import AnalysisService

router = APIRouter()

class Claim(BaseModel):
    claim: str
    uncommonness: int
    tag: str

class ClaimResponse(BaseModel):
    claims: List[Claim]

# Initialize AnalysisService
analysis_service = AnalysisService()

@router.post("/extract_claims", response_model=ClaimResponse)
async def extract_claims(request: FactCheckRequest, use_deepseek: bool = True):
    """
    Extract claims from text or URL content.
    
    Args:
        request (FactCheckRequest): Request containing text or URL
        use_deepseek (bool): Whether to use DeepSeek API instead of OpenAI
        
    Returns:
        ClaimResponse: List of extracted claims with uncommonness scores and tags
        
    Raises:
        HTTPException: If neither text nor URL is provided
    """
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Either text or URL must be provided")
    
    try:
        # For now, we only handle text input
        # TODO: Add URL content extraction
        text = request.text or ""
        if use_deepseek:
            claims = await analysis_service.deepseek_service.extract_claims(text)
        else:
            claims = await analysis_service.claim_extractor.extract_claims(text)
        
     
        
        return ClaimResponse(claims=claims)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting claims: {str(e)}")

@router.post("/check")
async def check_facts(request: FactCheckRequest, use_deepseek: bool = False):
    """
    Check facts from provided text or URL.
    
    Args:
        request (FactCheckRequest): Request containing text or URL
        use_deepseek (bool): Whether to use DeepSeek API instead of OpenAI
    """
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Either text or URL must be provided")
    
    try:
        # For now, we only handle text input
        # TODO: Add URL content extraction
        text = request.text or ""
        
        # Get sources (this is a placeholder - you should implement proper source retrieval)
        sources = []
        
        # Analyze text using the specified service
        result = await analysis_service.analyze_text(text, sources, use_deepseek=use_deepseek)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking facts: {str(e)}") 
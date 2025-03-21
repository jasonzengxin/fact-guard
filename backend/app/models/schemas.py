"""
Data models and schemas for the fact-checking service.
"""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from enum import Enum

class SourceType(str, Enum):
    """Types of sources that can be used for fact-checking"""
    NEWS = "news"
    ACADEMIC = "academic"
    BLOG = "blog"
    GOVERNMENT = "government"
    OTHER = "other"

class Source(BaseModel):
    """Represents a source used for fact-checking"""
    title: str
    snippet: str
    link: HttpUrl
    source_type: SourceType
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    citations: Optional[int] = None
    abstract: Optional[str] = None
    contribution_score: Optional[float] = None  # Score indicating how much this source contributes to the overall confidence

class Discrepancy(BaseModel):
    """Represents a discrepancy found between a claim and a source"""
    claim: str
    source: Source
    explanation: str

class FactCheckRequest(BaseModel):
    """Request model for fact-checking endpoint"""
    text: Optional[str] = None
    url: Optional[HttpUrl] = None

class FactCheckResponse(BaseModel):
    """Response model for fact-checking endpoint"""
    is_fact: bool
    confidence: float
    explanation: str
    sources: List[Source]
    academic_sources: List[Source] 
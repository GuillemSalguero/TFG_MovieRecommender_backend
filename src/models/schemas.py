from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=3)
    max_results: int = 5
    max_runtime: Optional[int] = None

class RAResult(BaseModel):
    title: Optional[str]
    year: Optional[str]
    genres: Optional[str]
    directors: Optional[str]
    runtime: Optional[int]
    score: float
    signals: dict
    snippets: List[str]
    poster: Optional[str] = None
    link: str

class RecommendResponse(BaseModel):
    query: str
    results: List[RAResult]

from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    include_sources: Optional[bool] = True

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[dict]] = None
    error: Optional[str] = None

class Document(BaseModel):
    text: str
    source: str
    page: str
    score: float
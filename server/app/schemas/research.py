
from pydantic import BaseModel
from typing import List, Optional

class ResearchRequest(BaseModel):
    query: str
    user_id: str
    skip_cache: bool = False

class Source(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None

class ResearchResponse(BaseModel):
    conversation_id: str
    query: str
    report: str
    sources: List[Source]
    search_queries: List[str]
    cached: bool = False

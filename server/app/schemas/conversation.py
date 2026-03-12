
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid 


class ConversationBase(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    # metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, alias='conversation_metadata')
    conversation_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, alias='conversation_metadata')

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    messages: Optional[List[Dict[str, Any]]] = None
    # metadata: Optional[Dict[str, Any]] = Field(None, alias='conversation_metadata')
    conversation_metadata: Optional[Dict[str, Any]] = None


class ConversationResponse(ConversationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class MessageAdd(BaseModel):
    role: str  # user, assistant, system
    content: str
    metadata: Optional[Dict[str, Any]] = None

class AgentLogCreate(BaseModel):
    conversation_id: uuid.UUID
    agent_type: str
    action: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    execution_time: int
    status: str

class AgentLogResponse(AgentLogCreate):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True






# import redis
# import json
# from typing import Any, Optional
# from app.core.config import settings

# class CacheService:
#     def __init__(self):
#         self.redis_client = redis.from_url(
#             settings.REDIS_URL,
#             decode_responses=True
#         )
    
#     def get(self, key: str) -> Optional[Any]:
#         """Get value from cache"""
#         try:
#             value = self.redis_client.get(key)
#             if value:
#                 return json.loads(value)
#             return None
#         except Exception as e:
#             print(f"Cache get error: {e}")
#             return None
    
#     def set(self, key: str, value: Any, expiry: int = 3600):
#         """Set value in cache with expiry"""
#         try:
#             self.redis_client.setex(
#                 key,
#                 expiry,
#                 json.dumps(value)
#             )
#         except Exception as e:
#             print(f"Cache set error: {e}")
    
#     def delete(self, key: str):
#         """Delete key from cache"""
#         try:
#             self.redis_client.delete(key)
#         except Exception as e:
#             print(f"Cache delete error: {e}")
    
#     def exists(self, key: str) -> bool:
#         """Check if key exists"""
#         try:
#             return self.redis_client.exists(key) > 0
#         except Exception as e:
#             print(f"Cache exists error: {e}")
#             return False

# cache_service = CacheService()

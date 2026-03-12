from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.conversation import (
    ConversationResponse,
    ConversationCreate,
    MessageAdd,
    AgentLogResponse,
)
from app.crud.conversation import ConversationCRUD, AgentLogCRUD
from app.agents.research_agent import ResearchAgentV3
from app.core.exceptions import (
    BaseAPIException,
    DatabaseException,
    AgentException,
    ValidationException,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/research", tags=["research"])


@router.post("/run", response_model=dict)
async def run_research(query: str, user_id: str, db: AsyncSession = Depends(get_db)):
    """Run research agent with full error handling"""
    try:
        if not query or not query.strip():
            raise ValidationException("Query cannot be empty")

        if not user_id or not user_id.strip():
            raise ValidationException("User ID is required")

        agent = ResearchAgentV3(db)
        result = await agent.run(query, user_id)

        return {
            "status": "success",
            "conversation_id": result.get("conversation_id"),
            "report": result.get("final_report"),
            "search_results": len(result.get("search_results", [])),
        }

    except ValidationException as e:
        raise e
    except AgentException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in research endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new conversation"""
    return await ConversationCRUD.create(db, conversation)


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    """Get conversation by ID"""
    return await ConversationCRUD.get_by_id(db, conversation_id)


@router.get("/conversations/user/{user_id}", response_model=List[ConversationResponse])
async def get_user_conversations(
    user_id: str, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    """Get all conversations for a user"""
    return await ConversationCRUD.get_user_conversations(db, user_id, skip, limit)


@router.post(
    "/conversations/{conversation_id}/messages", response_model=ConversationResponse
)
async def add_message(
    conversation_id: uuid.UUID, message: MessageAdd, db: AsyncSession = Depends(get_db)
):
    """Add a message to conversation"""
    return await ConversationCRUD.add_message(db, conversation_id, message.dict())


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    """Delete a conversation"""
    await ConversationCRUD.delete(db, conversation_id)
    return {"status": "deleted", "conversation_id": str(conversation_id)}


@router.get("/logs/{conversation_id}", response_model=List[AgentLogResponse])
async def get_conversation_logs(
    conversation_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get agent logs for a conversation"""
    return await AgentLogCRUD.get_conversation_logs(db, conversation_id, skip, limit)

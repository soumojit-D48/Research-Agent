from typing import List
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.conversation import (
    ConversationResponse,
    ConversationCreate,
    MessageAdd,
    AgentLogResponse,
)
from app.crud.conversation import (
    ConversationCRUD,
    AgentLogCRUD,
)

# -------------------------------------------------------------------
# Router
# -------------------------------------------------------------------

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)

# -------------------------------------------------------------------
# Conversation Endpoints
# -------------------------------------------------------------------

@router.post("", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new conversation."""
    return await ConversationCRUD.create(db, conversation)


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get conversation by ID."""
    return await ConversationCRUD.get_by_id(db, conversation_id)


@router.get("/user/{user_id}", response_model=List[ConversationResponse])
async def get_user_conversations(
    user_id: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """Get all conversations for a user."""
    return await ConversationCRUD.get_user_conversations(
        db,
        user_id,
        skip,
        limit,
    )


@router.post("/{conversation_id}/messages", response_model=ConversationResponse)
async def add_message(
    conversation_id: uuid.UUID,
    message: MessageAdd,
    db: AsyncSession = Depends(get_db),
):
    """Add a message to a conversation."""
    return await ConversationCRUD.add_message(
        db,
        conversation_id,
        message.dict(),
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation."""
    await ConversationCRUD.delete(db, conversation_id)
    return {
        "status": "deleted",
        "conversation_id": str(conversation_id),
    }

# -------------------------------------------------------------------
# Agent Logs
# -------------------------------------------------------------------

@router.get("/{conversation_id}/logs", response_model=List[AgentLogResponse])
async def get_conversation_logs(
    conversation_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get agent logs for a conversation."""
    return await AgentLogCRUD.get_conversation_logs(
        db,
        conversation_id,
        skip,
        limit,
    )

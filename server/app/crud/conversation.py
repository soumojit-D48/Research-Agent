
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.conversation import Conversation, AgentLog
from app.schemas.conversation import ConversationCreate, ConversationUpdate, AgentLogCreate
from app.core.exceptions import DatabaseException, ResourceNotFoundException

class ConversationCRUD:
    """CRUD operations for conversations"""
    
    @staticmethod
    async def create(db: AsyncSession, conversation: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        try:
            db_conversation = Conversation(
                id=uuid.uuid4(),
                user_id=conversation.user_id,
                session_id=conversation.session_id or str(uuid.uuid4()),
                messages=conversation.messages or [],
                conversation_metadata=conversation.conversation_metadata or {},
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(db_conversation)
            await db.commit()
            await db.refresh(db_conversation)
            
            return db_conversation
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Failed to create conversation: {str(e)}")
    
    @staticmethod
    async def get_by_id(db: AsyncSession, conversation_id: uuid.UUID) -> Conversation:
        """Get conversation by ID"""
        try:
            result = await db.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                raise ResourceNotFoundException(f"Conversation {conversation_id} not found")
            
            return conversation
            
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to fetch conversation: {str(e)}")
    
    @staticmethod
    async def get_by_session(db: AsyncSession, session_id: str) -> Optional[Conversation]:
        """Get conversation by session ID"""
        try:
            result = await db.execute(
                select(Conversation).where(Conversation.session_id == session_id)
            )
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to fetch conversation: {str(e)}")
    
    @staticmethod
    async def get_user_conversations(
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 10
    ) -> List[Conversation]:
        """Get all conversations for a user"""
        try:
            result = await db.execute(
                select(Conversation)
                .where(Conversation.user_id == user_id)
                .order_by(Conversation.updated_at.desc())
                .offset(skip)
                .limit(limit)
            )
            return list(result.scalars().all())
            
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to fetch conversations: {str(e)}")
    
    @staticmethod
    async def update(
        db: AsyncSession,
        conversation_id: uuid.UUID,
        conversation_update: ConversationUpdate
    ) -> Conversation:
        """Update a conversation"""
        try:
            # Check if exists
            await ConversationCRUD.get_by_id(db, conversation_id)
            
            # Update fields
            update_data = conversation_update.dict(exclude_unset=True)
            update_data['updated_at'] = datetime.utcnow()
            
            await db.execute(
                update(Conversation)
                .where(Conversation.id == conversation_id)
                .values(**update_data)
            )
            
            await db.commit()
            
            return await ConversationCRUD.get_by_id(db, conversation_id)
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Failed to update conversation: {str(e)}")
    
    @staticmethod
    async def add_message(
        db: AsyncSession,
        conversation_id: uuid.UUID,
        message: dict
    ) -> Conversation:
        """Add a message to conversation"""
        try:
            conversation = await ConversationCRUD.get_by_id(db, conversation_id)
            
            messages = conversation.messages or []
            messages.append({
                **message,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            await db.execute(
                update(Conversation)
                .where(Conversation.id == conversation_id)
                .values(messages=messages, updated_at=datetime.utcnow())
            )
            
            await db.commit()
            
            return await ConversationCRUD.get_by_id(db, conversation_id)
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Failed to add message: {str(e)}")
    
    @staticmethod
    async def delete(db: AsyncSession, conversation_id: uuid.UUID) -> bool:
        """Delete a conversation"""
        try:
            await ConversationCRUD.get_by_id(db, conversation_id)
            
            await db.execute(
                delete(Conversation).where(Conversation.id == conversation_id)
            )
            await db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Failed to delete conversation: {str(e)}")


class AgentLogCRUD:
    """CRUD operations for agent logs"""
    
    @staticmethod
    async def create(db: AsyncSession, log: AgentLogCreate) -> AgentLog:
        """Create an agent log entry"""
        try:
            db_log = AgentLog(
                id=uuid.uuid4(),
                conversation_id=log.conversation_id,
                agent_type=log.agent_type,
                action=log.action,
                input_data=log.input_data,
                output_data=log.output_data,
                execution_time=log.execution_time,
                status=log.status,
                created_at=datetime.utcnow()
            )
            
            db.add(db_log)
            await db.commit()
            await db.refresh(db_log)
            
            return db_log
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseException(f"Failed to create agent log: {str(e)}")
    
    @staticmethod
    async def get_conversation_logs(
        db: AsyncSession,
        conversation_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[AgentLog]:
        """Get all logs for a conversation"""
        try:
            result = await db.execute(
                select(AgentLog)
                .where(AgentLog.conversation_id == conversation_id)
                .order_by(AgentLog.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            return list(result.scalars().all())
            
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to fetch agent logs: {str(e)}")

from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.db.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, index=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    messages = Column(JSON, default=list)
    conversation_metadata = Column("metadata", JSON, default=dict)
    # conversation_metadata = Column('metadata', JSON, nullable=True)  # Renamed with column name preserved
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), index=True)
    agent_type = Column(String, nullable=False)
    action = Column(String, nullable=False)
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    execution_time = Column(Integer)  # milliseconds
    status = Column(String, nullable=False, index=True)  # success, error, timeout
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

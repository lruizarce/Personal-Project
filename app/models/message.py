from uuid import UUID, uuid4
from enum import StrEnum
from datetime import datetime as dt, timezone
from sqlmodel import SQLModel, Field


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Auto generated unique identifier for messages")
    conversation_id: UUID = Field(foreign_key="conversation.id", description="Foreign key to conversation")
    role: Role = Field(description="Message role")
    content: str = Field(description="Message content")
    input_tokens: int = Field(description="Tokens in (for user messages, including context)")
    output_tokens: int = Field(description="Tokens out (for assistant messages)")
    latency_ms: int = Field(description="Response time")
    model: str = Field(description="Actual model used")
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc), description="Timestamp when message was created")
    deleted_at: dt | None = Field(default=None, description="Timestamp when message was soft deleted")
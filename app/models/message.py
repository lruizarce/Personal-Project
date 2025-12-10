from uuid import UUID, uuid7
from enum import StrEnum
from typing import Annotated
from datetime import datetime as dt, timezone
from sqlmodel import SQLModel, Field


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    id: Annotated[UUID, Field(description="Auto generated unique identifier for messages. Primary Key", primary_key=True)] = Field(default_factory=uuid7)
    conversation_id: Annotated[UUID, Field(foreign_key="conversation.id", description="Foreign key to conversation")]
    role: Annotated[Role, Field(description="Message role")]
    context: Annotated[str, Field(description="Message content")]
    input_tokens: Annotated[int, Field(description="Tokens in (for user messages, including context)")]
    output_tokens: Annotated[int, Field(description="Tokens out (for assistant messages)")]
    latency_ms: Annotated[int, Field(description="Response time")]
    model: Annotated[str, Field(description="Actual model used")]
    created_at: Annotated[dt, Field(description="Timestamp when message was created")] = Field(default_factory=lambda: dt.now(timezone.utc))
    deleted_at: Annotated[dt | None, Field(description="Timestamp when conversation was soft deleted")] = None
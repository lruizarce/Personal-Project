from uuid import UUID, uuid7
from enum import StrEnum

from typing import Literal, Annotated
from datetime import datetime as dt, timezone
from sqlmodel import SQLModel, Field, Relationship


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class message(SQLModel, table=True):
    id: Annotated[UUID, Field(description="Auto generated unique identifier for messages. Primary Key", primary_key=True)] = Field(default_factory=uuid7)
    conversation_id: UUID = Field(foreign_key="conversation.id", description="Foreign key to conversation")
    role: Role
    context: str
    input_tokens: Annotated[int , Field(description="Tokens in (for user messages, including context)")]
    output_tokens: Annotated[int, Field(description="Tokens out (for assistant messages)")]
    latency_ms: Annotated[int, Field(description="Response time")]
    model: Annotated[str, Field(description="Actual model used")]
    created_at: Annotated[dt, Field(description="Timestamp when message was created")] = Field(default_factory=lambda: dt.now(timezone.utc))
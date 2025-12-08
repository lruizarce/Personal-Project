from sqlmodel import SQLModel, Field
from uuid import UUID, uuid7
from typing import Annotated
from datetime import datetime as dt, timezone

class Conversation(SQLModel, table=True):
    id: Annotated[UUID, Field(description="Auto generated unique identifier", primary_key=True)] = Field(default_factory=uuid7)
    user_id: Annotated[str | None, Field(description="Optional, for multi-user support")] = None
    title: Annotated[str, Field(description="Auto-generated or user-provided")] = "New Conversation"
    model: Annotated[str, Field(description="Default model for this conversation")] = "claude-sonnet-4-20250514"
    system_prompt: Annotated[str | None, Field(description="Optional system prompt override")] = None
    created_at: Annotated[dt, Field(description="Timestamp when conversation was created")] = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: Annotated[dt, Field(description="Timestamp when conversation was last updated")] = Field(default_factory=lambda: dt.now(timezone.utc))
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Annotated
from datetime import datetime as dt, timezone

class ConversationUpdate(SQLModel):
    title: str | None = None
    model: str | None = None
    system_prompt: str | None = None


class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Auto generated unique identifier")
    user_id: str | None = Field(default=None, description="Optional, for multi-user support")
    title: str = Field(default="New Conversation", description="Auto-generated or user-provided")
    model: str = Field(default="claude-sonnet-4-20250514", description="Default model for this conversation")
    system_prompt: str | None = Field(default=None, description="Optional system prompt override")
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc), description="Timestamp when conversation was created")
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc), description="Timestamp when conversation was last updated")
    deleted_at: dt | None = Field(default=None, description="Timestamp when conversation was soft deleted")
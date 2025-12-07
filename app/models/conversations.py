from uuid import UUID, uuid4
from datetime import datetime as dt, timezone
from pydantic import BaseModel, Field
from typing import Annotated

class Conversation(BaseModel):
    id: Annotated[UUID, Field(description="Auto generated unique identifier for the conversation")] = Field(default_factory=uuid4)
    user_id: Annotated[str | None, Field(description="Optional, for multi-user support")] = None
    title: Annotated[str, Field(description="Auto-generated or user-provided")] = "New Conversation"
    model: Annotated[str, Field(description="Default model for this conversation")] = "claude-sonnet-4-20250514"
    system_prompt: Annotated[str | None, Field(description="Optional system prompt override")] = None
    created_at: Annotated[dt, Field(description="Timestamp when conversation was created")] = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: Annotated[dt, Field(description="Timestamp when conversation was last updated")] = Field(default_factory=lambda: dt.now(timezone.utc))
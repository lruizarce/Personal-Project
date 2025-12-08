from uuid import UUID, uuid7
from enum import StrEnum
from typing import Annotated
from decimal import Decimal
from datetime import datetime as dt, timezone
from sqlmodel import SQLModel, Field


class Provider(StrEnum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    META = "meta"
    AMAZON = "amazon"


class UsageLog(SQLModel, table=True):
    id: Annotated[UUID, Field(description="Auto generated unique identifier", primary_key=True)] = Field(default_factory=uuid7)
    user_id: Annotated[str, Field(description="User identifier")]
    conversation_id: Annotated[UUID | None, Field(description="Optional reference to conversation")] = None
    model: Annotated[str, Field(description="Model used")]
    provider: Annotated[Provider, Field(description="AI provider")]
    input_tokens: Annotated[int, Field(ge=0, description="Input tokens used")]
    output_tokens: Annotated[int, Field(ge=0, description="Output tokens used")]
    estimated_cost: Annotated[Decimal, Field(ge=0, decimal_places=6, description="Estimated cost")]
    created_at: Annotated[dt, Field(description="Timestamp when log was created")] = Field(default_factory=lambda: dt.now(timezone.utc))
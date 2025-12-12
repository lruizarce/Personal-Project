from uuid import UUID, uuid4
from enum import StrEnum
from decimal import Decimal
from datetime import datetime as dt, timezone
from sqlmodel import SQLModel, Field


class Provider(StrEnum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    META = "meta"
    AMAZON = "amazon"


class UsageLog(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Auto generated unique identifier")
    user_id: str = Field(description="User identifier")
    conversation_id: UUID | None = Field(default=None, description="Optional reference to conversation")
    model: str = Field(description="Model used")
    provider: Provider = Field(description="AI provider")
    input_tokens: int = Field(ge=0, description="Input tokens used")
    output_tokens: int = Field(ge=0, description="Output tokens used")
    estimated_cost: Decimal = Field(ge=0, decimal_places=6, description="Estimated cost")
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc), description="Timestamp when log was created")
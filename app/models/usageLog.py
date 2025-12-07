from pydantic import Field, BaseModel
from uuid import UUID, uuid4
from typing import Annotated
from decimal import Decimal
from datetime import datetime as dt, timezone
from enum import StrEnum

class Provider(StrEnum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    META = "meta"
    AMAZON = "amazon"

class UsageLog(BaseModel):
    id: Annotated[UUID, Field(description="Usage log unique identifier")] = Field(default_factory=uuid4)
    user_id: Annotated[str, Field(description="User ID")]
    conversation_id: Annotated[UUID | None, Field(description="Optional FK to Conversation")] = None
    model: Annotated[str, Field(description="Model used for inference")]
    provider: Annotated[Provider, Field(description="Provider name")]
    input_tokens: Annotated[int, Field(ge=0, description="Input tokens")]
    output_tokens: Annotated[int, Field(ge=0, description="Output tokens")]
    estimated_cost: Annotated[Decimal, Field(ge=0, description="Estimated cost of inference")]
    created_at: Annotated[dt, Field(description="Log creation timestamp")] = Field(default_factory=lambda: dt.now(timezone.utc))
from uuid import UUID, uuid4
from datetime import datetime as dt, timezone
from typing import Annotated
from pydantic import BaseModel, Field

class VariableDefinition(BaseModel):
    name: Annotated[str, Field(description="Variable name")]
    description: Annotated[str, Field(description="What this variable is for")]
    required: Annotated[bool, Field(description="Whether variable is required")] = True

class PromptTemplate(BaseModel):
    id: Annotated[UUID, Field(description="Primary key")] = Field(default_factory=uuid4)
    name: Annotated[str, Field(description="Unique identifier for template")]
    description: Annotated[str | None, Field(description="What is the template for?")] = None
    content: Annotated[str, Field(description="Template with {{variable}} placeholders")]
    variables: Annotated[list[VariableDefinition], Field(description="Expected variables")] = []
    created_at: Annotated[dt, Field(description="Creation timestamp")] = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: Annotated[dt, Field(description="Last update timestamp")] = Field(default_factory=lambda: dt.now(timezone.utc))
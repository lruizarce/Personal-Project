from uuid import UUID, uuid7
from datetime import datetime as dt, timezone
from typing import Annotated
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, JSON


class VariableDefinition(BaseModel):
    name: str
    description: str
    required: bool = True


class PromptTemplate(SQLModel, table=True):
    id: Annotated[UUID, Field(description="Auto generated unique identifier", primary_key=True)] = Field(default_factory=uuid7)
    name: Annotated[str, Field(description="Unique identifier for template")]
    description: Annotated[str | None, Field(description="Optional description")] = None
    content: Annotated[str, Field(description="Template with {{variable}} placeholders")]
    variables: Annotated[list[VariableDefinition], Field(default=[], sa_column=Column(JSON))]
    created_at: Annotated[dt, Field(description="Timestamp when template was created")] = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: Annotated[dt, Field(description="Timestamp when template was last updated")] = Field(default_factory=lambda: dt.now(timezone.utc))